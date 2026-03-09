import random

class Choice:
    def __init__(self):
        self.choices = []

    def get_choices(self):
        return self.choices

    def add_choice(self, choice):
        self.choices.append(choice)

    def contains_choice(self, start_index, question_words : list):
        for choice in self.choices:
            value = choice.get_value().split()

            i = start_index
            while i < len(value) and i < len(question_words):
                if value[i] == question_words[i]:
                    return True
                i += 1
        return False

    def get_random(self):
        return random.choice(self.choices)