from contraintes.manager._base import BaseConstraintsManager
from contraintes.constraints._base import ConstraintsObject
from contraintes.hyperparameters.handler import HyperparametersHandler
from contraintes.tags.handler import TagsHandler
from contraintes.tags.master.evaluate_constraints import EvaluateConstraints


class ArnoConstraintsManager(BaseConstraintsManager):
    

    def __init__(self, 
        path_to_pipeline: str = None,
        constraints: ConstraintsObject = None, 
        ae_hyperparameters_handler: HyperparametersHandler = None,  
        cl_hyperparameters_handler: HyperparametersHandler = None,
        tags: TagsHandler = None
        ):

        super().__init__(constraints=constraints, path_to_pipeline=path_to_pipeline, tags=tags)

        self.ae_hyperparameters_handler = ae_hyperparameters_handler
        self.cl_hyperparameters_handler = cl_hyperparameters_handler

    def score(self):
        """
        compute the score of the hyperparameters
        """
        
        for tag in self.tags:
            if isinstance(tag, EvaluateConstraints):
                return tag.score()
