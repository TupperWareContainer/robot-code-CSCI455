from al_dialog_definition import Definition

class Program:
    def __init__(self):
        self.definitions = {}
        self.rules = []
        self.user_vars = {}

    def get_rules(self):
        return self.rules

    def get_definitions(self):
        return self.definitions

    def add_definition(self, name, choices):
        self.definitions[name] = Definition(name, choices)

    def add_user_var(self, name, value):
        self.user_vars[name] = value

    def get_user_var(self, name):
        return self.user_vars.get(name)