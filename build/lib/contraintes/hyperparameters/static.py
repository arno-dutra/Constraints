from contraintes.hyperparameters._base import BaseHyperparameter
import numpy as np


class StaticHyperparameter(BaseHyperparameter):
    def __init__(self, name, value, type = None):
        super().__init__(name, type)
        self.value = value

    def get_value(self, next: bool = True, **kwargs):
        yield self.type(self.value)

    def get_loop_size(self):
        return 1

    def __len__(self):
        return 1
        