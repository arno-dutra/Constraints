from contraintes.manager._base import BaseConstraintsManager
from contraintes.constraints._base import ConstraintsObject
from contraintes.hyperparameters.handler import HyperparametersHandler
from contraintes.tags.master.handler import TagsHandler
from contraintes.tags.master.evaluate_constraints import EvaluateConstraints
import pandas as pd
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

    def score(self):
        """
        compute the score of the hyperparameters
        """
        
        for tag in self.tags:
            if isinstance(tag, EvaluateConstraints):
                return tag.score(path=self.tags.path)

    def store(self, path: str, where: dict, score: dict = {}):
        """
        store the score of the hyperparameters

        Parameters
        ----------
        path : str
            the path to the file where to store the score
        where : str
            the keys values to find the right entry in the file
        score : dict
            the score of the hyperparameters given by the score method
        """
        
        df = pd.read_csv(path, sep=",", index_col=None)

        for k,v in score.items():
            df.loc[tuple([df[key] == value for key, value in where.items()] + [[k]])] = v

        df.to_csv(path, sep=",", index=False)
        
    def get_hyperparameters_loop_size(self):
        """
        get the number of hyperparameters combinations
        """
        return self.ae_hyperparameters_handler.get_loop_size() * self.cl_hyperparameters_handler.get_loop_size()
        
    def rename_dialogue(self):
        # Transform the name of the file from ./example/dialogue.json to 
        # ./example/__dialogue_ResNetEncoder_MNIST_1234567890.json

        a = self.tags.get("model_file_name")
        a = a.split("_")
        a[2] = ".".join(self.tags.path.split("/")[-1].split(".")[:-1])
        a = "_".join(a)
        ext = self.tags.path.split("/")[-1].split(".")[-1]
        new_name = "/".join(self.tags.path.split("/")[:-1]) + f"/{a}.{ext}"

        os.rename(self.tags.path, new_name)
    
    def run_pipeline(self, model, dataset, other={}, new_hyperparameters=True):
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
                    "cmmp": self.tags.path,
                    "other": o
                })
            
            os.system(command)
        
        elif new_hyperparameters == "iter":
            loop_size = self.ae_hyperparameters_handler.get_loop_size() * self.cl_hyperparameters_handler.get_loop_size()
            i = 1
            for aeh in self.ae_hyperparameters_handler:
                for clh in self.cl_hyperparameters_handler:
                    print("="*100, f"Starting a new pipeline with hyperparameters set {i}/{loop_size}")
                    
                    self.tags.generate_hash(hyperparameters=[aeh, clh])
                    self.tags.send_message()

                    command = (f"python {self.path_to_pipeline} {dataset} {model} " \
                        "--autoencoder-hyperparameters '%(aeh)s' " \
                        "--clustering-hyperparameters '%(clh)s' " \
                        "--constraints-manager-messenger-path %(cmmp)s " \
                        "%(other)s" % 
                        {
                            "aeh": json.dumps(aeh),
                            "clh": json.dumps(clh),
                            "cmmp": self.tags.path,
                            "other": o
                        })
                    
                    os.system(command)

                    self.store(path=f"./local/__resultats_{model}.csv", where={"model_file_name": self.tags.get("model_file_name")}, score=self.score())
                    self.store(path=f"./local/__resultats_{model}.csv", where={"model_file_name": self.tags.get("model_file_name")}, score=self.constraints.get_constraints())

                    self.rename_dialogue()

                    i += 1
                    