from contraintes.constraints._base import ConstraintsObject
from contraintes.tags.master.handler import TagsHandler
from contraintes.tags.master.evaluate_constraints import EvaluateConstraints
import os
import json
import pandas as pd
from copy import deepcopy
import numpy as np


class BaseConstraintsManager:
    """
    root class for all constraints managers
    """

    def __init__(self, constraints: ConstraintsObject = None, path_to_pipeline: str = None, tags: TagsHandler = None, check_overconstrained=True):
        self.constraints = constraints

        if check_overconstrained and self.constraints is not None:
            if self.constraints.is_overconstrained():
                Warning("The problem is overconstrained.")

        self.path_to_pipeline = path_to_pipeline
        self.tags = tags
        
    def run_pipeline(self, model, dataset, other={}, new_hyperparameters=True):
        """
        run the model pipeline
        """
        o = ""
        for k, v in other.items():
            o += f"--{k} {v} "

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


    def score(self):
        """
        compute the score of the hyperparameters
        """
        rep = []
        for tag in self.tags:
            if isinstance(tag, EvaluateConstraints):
                rep.append(tag.score(path=self.tags.get_path()))
        print("/////////////////////////////// Leaving score ///////////////////////////////")
        if len(rep) == 1:
            return rep[0]
        return rep

    def store(self, path: str, where: dict, score: dict or list = {}):
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

        if isinstance(score, dict):
            score = [score]



        # Duplicate the line corresponding to the where keys values and add the score of each constraints set contained in the score list
        INDEX = pd.Series([True] * len(df))
        for key, value in where.items():
            
            INDEX = INDEX & (df[key] == value)

        row = df.T.pop(INDEX.to_numpy().nonzero()[0][0])

        rs = []
        for s in score:
            r = row.copy()
            for k, v in s.items():
                r[k] = v
                r["from_duplicated"] = True
            rs.append(r.to_frame().T)

        df = pd.concat([df] + rs, axis=0)

                

        df.to_csv(path, sep=",", index=False)
        
        
    def get_hyperparameters_loop_size(self):
        """
        get the number of hyperparameters combinations
        """
        return self.ae_hyperparameters_handler.get_loop_size() * self.cl_hyperparameters_handler.get_loop_size()
    
    def _new_name_dialogue(self, model, dataset, full_path=False):

        new_name = f"dialogue_{model}_{dataset}_{self.tags.get_hash()}.json"

        if full_path:
            folder = "/".join(self.tags.get_path().split("/")[:-1]) + "/"
            new_name = folder + new_name

        return new_name

    def rename_dialogue(self, model, dataset):
        # Transform the name of the file from ./example/dialogue.json to 
        # ./example/__dialogue_ResNetEncoder_MNIST_1234567890.json

        new_name = self._new_name_dialogue(model, dataset, full_path=True)

        os.rename(self.tags.get_path(), new_name)

    def _iter(self, ae_hyperparameters_handler, cl_hyperparameters_handler, shuffle=True):
        
        l = []

        for aeh in ae_hyperparameters_handler:
            for clh in cl_hyperparameters_handler:
                l.append({"aeh": deepcopy(aeh), "clh": deepcopy(clh)})

        if shuffle:
            np.random.shuffle(l)

        for d in l:
            yield d["aeh"], d["clh"]

    def _run_already_done(self, model, dataset):

        if os.path.exists(self._new_name_dialogue(model, dataset, full_path=True)):
            return True
        else:
            return False

    def _run_already_in_progress(self):

        if os.path.exists(self.tags.get_path()):
            return True
        else:
            return False