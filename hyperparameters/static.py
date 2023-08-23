from contraintes.hyperparameters._base import BaseHyperparameter
import numpy as np


class StaticHyperparameter(BaseHyperparameter):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def get_value(self, next: bool = True):
        return self.value
