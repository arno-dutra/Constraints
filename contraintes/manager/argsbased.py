from contraintes.manager._base import BaseConstraintsManager
from contraintes.constraints._base import ConstraintsObject
from contraintes.hyperparameters.handler import HyperparametersHandler
from contraintes.tags.master.handler import TagsHandler
from contraintes.tags.master.evaluate_constraints import EvaluateConstraints
import json
import os


class ArgsBasedConstraintsManager(BaseConstraintsManager):
    

    def __init__(self, 
        path_to_pipeline: str = None,
        constraints: ConstraintsObject = None, 
        ae_hyperparameters_handler: HyperparametersHandler = None,  
        cl_hyperparameters_handler: HyperparametersHandler = None,
        tags: TagsHandler = None,
        check_overconstrained=True
        ):

        super().__init__(constraints=constraints, path_to_pipeline=path_to_pipeline, tags=tags, check_overconstrained=check_overconstrained)

        self.ae_hyperparameters_handler = ae_hyperparameters_handler
        self.cl_hyperparameters_handler = cl_hyperparameters_handler

    def run_pipeline(self, model, dataset, other={}, new_hyperparameters=True, shuffle=True):
        """
        run the model pipeline
        """
        o = ""
        for k, v in other.items():
            o += f"--{k} {v} "

        if new_hyperparameters == True:

            command = (f"python {self.path_to_pipeline} {dataset} {model} " \
                "--autoencoder-hyperparameters '%(aeh)s' " \
                "--clustering-hyperparameters '%(clh)s' " \
                "--constraints-manager-messenger-path %(cmmp)s " \
                "%(other)s" % 
                {
                    "aeh": json.dumps(self.ae_hyperparameters_handler.get_hyperparameters(next=new_hyperparameters)),
                    "clh": json.dumps(self.cl_hyperparameters_handler.get_hyperparameters(next=new_hyperparameters)),
                    "cmmp": self.tags.get_path(),
                    "other": o
                })
            
            os.system(command)
        
        elif new_hyperparameters == "iter":
            loop_size = self.ae_hyperparameters_handler.get_loop_size() * self.cl_hyperparameters_handler.get_loop_size()
            i = 1
            for aeh, clh in self._iter(self.ae_hyperparameters_handler, self.cl_hyperparameters_handler, shuffle=shuffle):
                print("="*100, f"Starting a new pipeline with hyperparameters set {i}/{loop_size}", end="")
                
                self.tags.generate_hash(hyperparameters=[aeh, clh])

                if self._run_already_done(model=model, dataset=dataset):
                    print("  --> Pipeline with hash %(h)s already done : skipping" % {"h": self.tags.get_hash()})
                    i += 1
                    continue
                if self._run_already_in_progress():
                    print("  --> Pipeline with hash %(h)s already in progress : skipping" % {"h": self.tags.get_hash()})
                    i += 1
                    continue
                print()

                self.tags.send_message()
        
                _aeh = ""
                for k, v in aeh.items():
                    _aeh += f"--{k} {v} "


                command = (f"python {self.path_to_pipeline} " \
                    "%(aeh)s "
                    "--hyperparameters_hash '%(hash)s' " \
                    "--clustering-hyperparameters '%(clh)s' " \
                    "--constraints-manager-messenger-path %(cmmp)s " \
                    "%(other)s" % 
                    {
                        "aeh": _aeh,
                        "clh": json.dumps(clh),
                        "cmmp": self.tags.get_path(),
                        "other": o % {"hash": self.tags.get_hash()},
                        "hash": self.tags.get_hash()
                    })
                
                os.system(command)

                print("/////////////////////////// Leaving subprocess ///////////////////////////")

                self.store(path=f"./local/__resultats_{model}.csv", where={"hash": self.tags.get_hash()}, score=self.score())

                print("/////////////////////////// Leaving storing ///////////////////////////")

                # self.store(path=f"./local/__resultats_{model}.csv", where={"hash": self.tags.get_hash()}, score=self.constraints.get_constraints())

                self.rename_dialogue(model=model, dataset=dataset)

                i += 1
                    