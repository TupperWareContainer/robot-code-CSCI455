import random

class Choice:
    def __init__(self):
        self.choices = []

    def get_choices(self):
        return self.choices

    def add_choice(self, choice):
        self.choices.append(choice)

    def get_random(self):
        return random.choice(self.choices)