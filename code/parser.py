from typing import Optional
from token import Token
from token_type import TokenType

class Parser:
    token_list : list

    def __init__(self, token_list):
        self.token_list = token_list

    def parse(self):
        for i in range(len(self.token_list)):
            token = self.token_list[i]

            if token.get_token_type() is TokenType.STRING:
                self._parse_attribute(i)
            elif token.get_token_type() is TokenType.VAR:
                pass
        return

    def _parse_attribute(self, i):
        next_token = self.get_next_token(i)
        return




    def parse_string(self):
        pass

    def get_next_token(self, cur_index) -> Optional[Token]:
        next_index = cur_index + 1

        if next_index < len(self.token_list):
            return self.token_list[cur_index]
        else:
            return None