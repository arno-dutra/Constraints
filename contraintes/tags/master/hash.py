from contraintes.tags.master._base import _BaseMaster
import hashlib


class HashTag(_BaseMaster):
    """
    Tag master for constantSender tag 

    Parameters
    ----------
    name : str
        name of the tag
    """
    def __init__(self, name="HashTag"):
        super().__init__(name)

    def set_hyperparameters(self, hyperparameters):
        
        sha = hashlib.sha256()
        sha.update("".join([str(x) for x in hyperparameters]).encode())
        self.hash = sha.hexdigest()

    def get_hash(self):
        """
        return the hash of the hyperparameters
        """
        if not isinstance(self.hash, str):
            raise ValueError("You must set the hyperparameters and compute the hash before getting the hash.")
        return self.hash

    def prepare_message(self):
        
        datas = {}

        datas["hash"] = self.hash

        return self.name, datas
