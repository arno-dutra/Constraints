import json


class _BaseMaster:
    def __init__(self, name):
        self.name = name
        self.answer = None

    def read_answer(self, path):
        """
        Read the answer message from the file
        """
        f = open(path, "r")

        lines = f.readlines()  # Skip the first line

        f.close()

        lines = lines[lines.index("=" * 100 + "\n") + 2:]  # Skip input message
        l = []
        for line in lines:
            if line == "\n":
                continue
            d = json.loads(line)
            if self.name in d:  # Check if the message is for this tag
                l.append(d[self.name])
        
        self.answer = l
