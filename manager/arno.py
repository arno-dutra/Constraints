from contraintes.manager._base import BaseConstraintsManager
from contraintes.generator._base import ConstraintsObject


class ArnoConstraintsManager(BaseConstraintsManager):
    

    def __init__(self, constraints: ConstraintsObject = None):
        super().__init__(constraints)