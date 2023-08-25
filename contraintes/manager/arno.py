from contraintes.manager._base import BaseConstraintsManager
from contraintes.constraints._base import ConstraintsObject
from contraintes.hyperparameters.handler import HyperparametersHandler
from contraintes.tags.master.handler import TagsHandler
from contraintes.tags.master.evaluate_constraints import EvaluateConstraints
import pandas as pd


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

        dff = df
        for key, value in where.items():
            dff = dff[dff[key] == value]
        
        for key, value in score.items():
            dff[key] = value

        dff.to_csv(path, sep=",", index=False)
        