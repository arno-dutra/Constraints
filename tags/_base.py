


class BaseTag:
    def __init__(self, name, path):
        self.name = name
        
        # JSON file
        f = open (path, "r")
        
        # Reading from file
        data = json.loads(f.read())
        f.close()

        self.msg = data[self.name]


    def send(self, **kwargs):
        buffer_size = 0 # This makes it so changes appear without buffering
        with open('output.log', 'a', buffer_size) as f:

            f.write(json.dumps({self.name: kwargs}) + '\n')
        
        f.close()
