


class BaseHyperparameter:

    def __init__(self, name, type = None):
        self.name = name
        self.frozen = False
        if type is None:
            type = lambda x: x
        self.type = type

    def get_value(self):
        """
        Return a value for the hyperparameter according to its distribution
        """
        ...
    
    def set_parameter(self, parameter,value):
        setattr(self, parameter, value)
    
class ArrayHyperparameter(BaseHyperparameter):

    def __init__(self, name, hyperparameters):
        super().__init__(name)
        self.hyperparameters = hyperparameters

    def get_value(self, next: bool or list = True):
        """
        Return a value for each hyperparameter in a list according to its distribution
        """
        if isinstance(next, bool):
            next = [next for _ in self.hyperparameters]

        return [d.get_value(n) for d, n in zip(self.hyperparameters, next)]