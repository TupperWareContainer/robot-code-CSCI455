from robot_token_type import TokenType

class Token:
    value : str
    token_type : TokenType

    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type

    def get_value(self):
        return self.value

    def get_token_type(self):
        return self.token_type