from contraintes.hyperparameters._base import BaseHyperparameter


class FromListHyperparameter(BaseHyperparameter):

    def __init__(self, name, values: list = []):
        super().__init__(name)

        if not all([v+v == 2*v for v in values]):
            raise ValueError("All values must be of a number-like type")

        self.values = values

        self.i = 0

    def get_value(self, next: bool = True):
        if not self.frozen and next:
            
            self.i += 1
            if self.i + 1 >= len(self.values):
                Warning("You are trying to get a value from a list of values that is too short. The list will be looped.")
                self.i %= len(self.values)

        return self.values[self.i]
    