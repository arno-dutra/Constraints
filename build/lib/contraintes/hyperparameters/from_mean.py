from contraintes.hyperparameters._base import BaseHyperparameter
import numpy as np


class FromMeanHyperparameter(BaseHyperparameter):
    def __init__(self, name, mean, std, type = None, size: int = 5):
        super().__init__(name, type)
        self.mean = mean
        self.std = std
        self.loop_size = size
        self.size = size
        
        self.previous_value = mean

    def get_value(self, next: bool = True, **kwargs):
        if not self.frozen and next:
            self.previous_value = np.random.normal(self.mean, self.std)
        yield self.type(self.previous_value)

    def get_loop_size(self):
        return self.loop_size

    def __len__(self):
        return self.size