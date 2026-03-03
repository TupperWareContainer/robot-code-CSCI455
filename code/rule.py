class Rule:
    def __init__(self, level, pattern, output):
        self.level = level
        self.pattern = pattern
        self.output = output
        self.children = []
        self.actions = []

    def get_level(self):
        return self.level

    def get_pattern(self):
        return self.pattern

    def get_output(self):
        return self.output

    def get_children(self):
        return self.children

    def get_actions(self):
        return self.actions

    def set_actions(self, actions):
        self.actions = actions