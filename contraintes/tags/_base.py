import json
import numpy as np


class _BaseTag:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        
        # JSON file
        f = open(self.path, "r")
        
        # Reading from file
        data = json.loads(f.read().split("\n%(sep)s\n\n" % {"sep": "=" * 100})[0])
        f.close()

        self.msg = data["tags"][self.name]


    def send(self, **kwargs):

        d = {self.name: standardize_types(kwargs)}
        txt = json.dumps(d) + '\n'

        with open(self.path, 'a') as f:
            print("Sending datas :", txt)
            f.write(txt)
        
        f.close()

def standardize_types(d: dict):

    for k, v in d.items():

        if isinstance(v, dict):
            d[k] = standardize_types(v)

        else:
            d[k] = np.array(v).tolist()

    return d