from token_type import TokenType

class Parser:
    token_list : list

    def __init__(self, token_list):
        self.token_list = token_list

    def parse(self):
        for token in self.token_list:
            if token.get_token_type() is TokenType.STRING:
                pass
            elif token.get_token_type() is TokenType.VAR:
                pass
        return