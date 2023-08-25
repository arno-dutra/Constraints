from contraintes.hyperparameters._base import BaseHyperparameter
import numpy as np


class FromMeanHyperparameter(BaseHyperparameter):
    def __init__(self, name, mean, std):
        super().__init__(name)
        self.mean = mean
        self.std = std
        
        self.previous_value = mean

    def get_value(self, next: bool = True):
        if not self.frozen and next:
            self.previous_value = np.random.normal(self.mean, self.std)
        return self.previous_value
