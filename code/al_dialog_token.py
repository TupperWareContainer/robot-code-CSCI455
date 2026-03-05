from al_dialog_token_type import TokenType

class Token:
    value : str
    token_type : TokenType
    line_num : int

    def __init__(self, value, token_type, line_num):
        self.value = value
        self.token_type = token_type
        self.line_num = line_num

    def get_value(self):
        return self.value

    def get_token_type(self):
        return self.token_type

    def get_line_num(self):
        return self.line_num