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

            # Check if all words in this choice match the segment in question_words
            if len(value) + start_index <= len(question_words) and all(
                    value[i] == question_words[start_index + i] for i in range(len(value))
            ):
                return True
        return False

    def get_random(self):
        return random.choice(self.choices)