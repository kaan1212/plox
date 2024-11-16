class Environment:
    def __init__(self):
        self.values = {}

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise RuntimeError(name, "Undefined variable'" + name.lexeme + "'.")

    def define(self, name, value):
        self.values[name] = value
