from contraintes.tags.master._base import _BaseMaster


class ConstantSender(_BaseMaster):
    """
    Tag master for constantSender tag 

    Parameters
    ----------
    name : str
        name of the tag
    ask_for : list
        list of the constant to ask for
    """
    def __init__(self, name="ConstantSender", ask_for=[]):
        super().__init__(name)

        self.ask_for = ask_for

    def prepare_message(self):
        
        datas = {}

        datas["ask_for"] = self.ask_for

        return self.name, datas

    def get(self, name, path=None):
        """
        return the value of the constant
        """
        
        self.read_answer(path)

        d = self.answer[0]
        for i in range(1, len(self.answer)):
            d.update(self.answer[i])

        return d[name]
