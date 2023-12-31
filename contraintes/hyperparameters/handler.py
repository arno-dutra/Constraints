from contraintes.hyperparameters._base import BaseHyperparameter
from contraintes.hyperparameters._base import ArrayHyperparameter
from contraintes.hyperparameters.from_list import FromListHyperparameter
from tabulate import tabulate
from copy import deepcopy


class HyperparametersHandler:

    def __init__(self, hyperparameters: list = []):

        if not all([isinstance(h, BaseHyperparameter) for h in hyperparameters]):
            raise ValueError("All hyperparameters must inherite from type BaseHyperparameter")

        self.hyperparameters = {h.name: h for h in hyperparameters}
        if len(self.hyperparameters) != len(hyperparameters):
            raise ValueError("All hyperparameters must have different names")


    def get_hyperparameters(self, next: bool = True, verbose: bool = True):
        datas = [[h, h.get_value(next)] for h in self.hyperparameters.values()]

        if verbose:
            print(tabulate([[h.name, v] for h, v in datas], headers=['Hyperparameter', 'Value']))

        return {h.name: v for h, v in datas}
    
    def add_hyperparameter(self, hyperparameter: BaseHyperparameter):
        if not isinstance(hyperparameter, BaseHyperparameter):
            raise ValueError("All hyperparameters must inherite from type BaseHyperparameter")
        if hyperparameter.name in self.hyperparameters:
            raise ValueError("{hyperparameter.name} is already in the hyperparameters list")

        self.hyperparameters.update({hyperparameter.name: hyperparameter}) 

    def get_loop_size(self):
        s = 1
        for h in self.hyperparameters.values():
            s *= h.get_loop_size()

        return s

    def __iter__(self):

        l = list(self.hyperparameters.values())

        yield from self._iter(l, {})
    
    def _iter(self, l, values):
        if len(l) == 0:
            yield values
        else:
            h = l[0]

            for v in h.get_value(iter=True):
                values[h.name] = v
                yield from self._iter(l[1:], values)