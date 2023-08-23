from contraintes.hyperparameters._base import BaseHyperparameter
from tabulate import tabulate


class HyperparametersHandler:

    def __init__(self, hyperparameters: list = []):

        if not all([isinstance(h, BaseHyperparameter) for h in hyperparameters]):
            raise ValueError("All hyperparameters must inherite from type BaseHyperparameter")

        self.hyperparameters = {h.name: h for h in hyperparameters}
        if len(self.hyperparameters) != len(hyperparameters):
            raise ValueError("All hyperparameters must have different names")


    def get_hyperparameters(self, next: bool = True, verbose: bool = True):
        datas = [[h, h.get_value(next)] for h in self.hyperparameters]

        if verbose:
            print(tabulate([[h.name, v] for h, v in datas], headers=['Hyperparameter', 'Value']))

        return {h.name: v for h, v in datas}
    
    def add_hyperparameter(self, hyperparameter: BaseHyperparameter):
        if not isinstance(hyperparameter, BaseHyperparameter):
            raise ValueError("All hyperparameters must inherite from type BaseHyperparameter")
        if hyperparameter.name in self.hyperparameters:
            raise ValueError("{hyperparameter.name} is already in the hyperparameters list")

        self.hyperparameters.append(hyperparameter) 