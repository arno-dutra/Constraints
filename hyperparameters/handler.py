from contraintes.hyperparameters._base import BaseHyperparameter
from tabulate import tabulate


class HyperparametersHandler:

    def __init__(self, hyperparameters: list = []):

        if not all([isinstance(h, BaseHyperparameter) for h in hyperparameters]):
            raise ValueError("All hyperparameters must inherite from type BaseHyperparameter")

        self.hyperparameters = hyperparameters


    def get_values(self):
        datas = [[h, h.get_value()] for h in self.hyperparameters]

        print(tabulate([[h.name, v] for h, v in datas], headers=['Hyperparameter', 'Value']))

        return {h.name: v for h, v in datas}
    