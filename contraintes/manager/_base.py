from contraintes.constraints._base import ConstraintsObject
from contraintes.tags.master.handler import TagsHandler
import os
import json


class BaseConstraintsManager:
    """
    root class for all constraint managers
    """

    def __init__(self, constraints: ConstraintsObject = None, path_to_pipeline: str = None, tags: TagsHandler = None, check_overconstrained=True):
        self.constraints = constraints

        if check_overconstrained and self.constraints is not None:
            if self.constraints.is_overconstrained():
                Warning("The problem is overconstrained.")

        self.path_to_pipeline = path_to_pipeline
        self.tags = tags
        
    def run_pipeline(self, model, dataset):
        """
        run the model pipeline
        """

        command = (f"python {self.path_to_pipeline} {dataset} {model} " \
            "--autoencoder-hyperparameters %(aeh)s " \
            "--clustering-hyperparameters %(clh)s " \
            "--constraints-manager-messenger-path %(cmmp)s" % 
            {
                "aeh": json.dumps(self.ae_hyperparameters_handler.get_hyperparameters(next=False)),
                "clh": json.dumps(self.cl_hyperparameters_handler.get_hyperparameters(next=False)),
                "cmmp": self.tags.path
            })
        
        os.system(command)
