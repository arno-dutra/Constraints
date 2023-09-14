from contraintes.manager._base import BaseConstraintsManager
from contraintes.constraints._base import ConstraintsObject
from contraintes.hyperparameters.handler import HyperparametersHandler
from contraintes.tags.master.handler import TagsHandler
from contraintes.tags.master.evaluate_constraints import EvaluateConstraints
import json
import os


class ArnoConstraintsManager(BaseConstraintsManager):
    

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
                
                flag = True
                while flag:
                    try: 

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

                        command = (f"python {self.path_to_pipeline} {dataset} {model} " \
                            "--autoencoder-hyperparameters '%(aeh)s' " \
                            "--clustering-hyperparameters '%(clh)s' " \
                            "--constraints-manager-messenger-path %(cmmp)s " \
                            "%(other)s" % 
                            {
                                "aeh": json.dumps(aeh),
                                "clh": json.dumps(clh),
                                "cmmp": self.tags.get_path(),
                                "other": o
                            })
                        
                        os.system(command)

                        self.store(path=self.tags.get("path"), where={"model_file_name": self.tags.get("model_file_name")}, score=self.score())
                        # self.store(path=f"./local/__resultats_{model}.csv", where={"model_file_name": self.tags.get("model_file_name")}, score=self.constraints.get_constraints())

                        self.rename_dialogue(model=model, dataset=dataset)

                        i += 1

                    except Exception as e:
                        print("  --> Pipeline with hash %(h)s failed : retrying" % {"h": self.tags.get_hash()})
                        print("  -->", e)
                        os.remove(self.tags.get_path())
                        continue
                    else:
                        flag = False