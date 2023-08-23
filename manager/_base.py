from contraintes.generator._base import ConstraintsObject


class BaseConstraintsManager:
    """
    root class for all constraint managers
    """

    def __init__(self, constraints: ConstraintsObject = None):
        self.constraints = constraints

        if self.constraints.is_overconstrained():
            Warning("The problem is overconstrained.")
        
        