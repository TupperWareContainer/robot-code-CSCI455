class Definition:
    def __init__(self, name, choices):
        self.name = name
        self.choices = choices

    def get_name(self):
        return self.name

    def get_choices(self):
        return self.choices