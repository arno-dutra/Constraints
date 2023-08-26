


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

    def __len__(self):
        raise NotImplementedError
    
class ArrayHyperparameter(BaseHyperparameter):

    def __init__(self, name, hyperparameters: list = []):
        super().__init__(name)
        self.hyperparameters = hyperparameters

    def get_value(self, next: bool or list = True, iter=False, **kwargs):
        """
        Return a value for each hyperparameter in a list according to its distribution
        """
        if not iter:
            if isinstance(next, bool):
                next = [next for _ in self.hyperparameters]

            return [d.get_value(n) for d, n in zip(self.hyperparameters, next)]

        else:
            yield from self._iter(self.hyperparameters, {})
    
    def _iter(self, l, values):
        if len(l) == 0:
            yield list(values.values())
        else:
            h = l[0]

            for v in h.get_value(iter=True):
                values[h.name] = v
                yield from self._iter(l[1:], values)

    def get_loop_size(self):
        s = 1
        for h in self.hyperparameters:
            s *= h.get_loop_size()

        return s

    def __len__(self):
        return len(self.hyperparameters)