


class BaseHyperparameter:

    def __init__(self, name):
        self.name = name
        self.frozen = False

    def get_value(self):
        """
        Return a value for the hyperparameter according to its distribution
        """
        ...
    
    def set_parameter(self, parameter,value):
        setattr(self, parameter, value)
    