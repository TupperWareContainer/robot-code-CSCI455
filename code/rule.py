class Rule:
    def __init__(self, level, pattern, output):
        self.level = level
        self.pattern = pattern
        self.output = output
        self.children = []

    def get_level(self):
        return self.level

    def get_pattern(self):
        return self.pattern

    def get_output(self):
        return self.output

    def get_children(self):
        return self.children