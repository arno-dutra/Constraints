from contraintes.tags.master._base import _BaseMaster
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

        with open(self.path, "w") as f:
            f.write(json.dumps(msg) + "\n%(sep)s\n\n" % {"sep": "=" * 100})

    def __iter__(self):
        return iter(self.tags)

