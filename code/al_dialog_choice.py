import random

class Choice:
    def __init__(self):
        self.choices = []

    def get_choices(self):
        return self.choices

    def add_choice(self, choice):
        self.choices.append(choice)

    def contains_choice(self, user_input : str):
        for choice_token in self.choices:
            choice = choice_token.get_value()

            if user_input in choice:
                return True
        return False

    def get_random(self):
        return random.choice(self.choices)