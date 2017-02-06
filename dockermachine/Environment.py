
class Environment:

    def __init__(self):
        self.mappings = {}

    def add(self, key, value):
        self.mappings[key] = value
