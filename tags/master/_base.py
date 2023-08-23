


class _BaseMaster:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.answer = None

    def read_answer(self):
        """
        Read the answer message from the file
        """
        f = open(self.path, "r")

        lines = f.readlines()  # Skip the first line
        
        f.close()

        lines = lines[f.index("=" * 100 + "\n") + 1:]  # Skip input message
        l = []
        for line in lines:
            if line == "\n":
                continue
            d = json.loads(line)
            if self.name in d:  # Check if the message is for this tag
                l.append(d[self.name])
        
        self.answer = l
