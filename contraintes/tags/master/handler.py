from contraintes.tags.master._base import _BaseMaster
from contraintes.tags.master.constant import ConstantSender
from contraintes.tags.master.hash import HashTag
import json


class TagsHandler:

    def __init__(self, path):
        self.path = path
        self.tags = []

    def add_tag(self, tag):
        """
        Add a tag to the list of tags
        """
        self.tags.append(tag)

    def send_message(self):
        """
        Send the message to the server
        """
        msg = {"tags": {}}
        for tag in self.tags:
            tag_name, tag_message = tag.prepare_message()
            msg["tags"][tag_name] = tag_message

        with open(self.get_path(), "w") as f:
            f.write(json.dumps(msg) + "\n%(sep)s\n\n" % {"sep": "=" * 100})
        f.close()

    def __iter__(self):
        return iter(self.tags)

    def get(self, name):
        """
        return the value of the constant
        """

        for tag in self.tags:
            if isinstance(tag, ConstantSender):
                if name in tag.ask_for:
                    return tag.get(name, path=self.get_path())

    def get_path(self):
        return self.path % {"hash": self.get_hash()}

    def get_hash(self):
        """
        return the hash of the hyperparameters
        """
        for tag in self.tags:
            if isinstance(tag, HashTag):
                return tag.get_hash()

    def generate_hash(self, hyperparameters):
        """
        Generate the hash of the hyperparameters
        """
        for tag in self.tags:
            if isinstance(tag, HashTag):
                tag.set_hyperparameters(hyperparameters)
                
