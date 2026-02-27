from token_type import TokenType
from token import Token

def _require(char, required_char):
    if char != required_char:
        print("Error: Invalid character expected:", required_char)
        return False
    return True

class Tokenizer:
    file_path : str
    pose : int
    token_list : list

    def __init__(self, file_path):
        self.file_path = file_path
        self.pose = 0
        self.token_list = []

    def parse(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self._tokenize_line(file)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} does not exist")
        except IOError:
            print(f"Error: An I/O error occurred when reading the file at '{self.file_path}'")

    def _tokenize_line(self, file):
        for line in file:
            line = line.strip()

            while self.pose < len(line):
                char : str = line[self.pose]

                if char == '#' or not line:
                    continue
                elif char == '"':
                    self._tokenize_str_with_quotes(line)
                elif char.isalpha() or char.isdigit():
                    self._tokenize_str_without_quotes(line)
                elif char == '&':
                    self._tokenize_var(line, TokenType.VAR)
                elif char == '~':
                    self._tokenize_var(line, TokenType.DEFINITION)
                elif char == '_':
                    token = Token(char, TokenType.VAR_CAPTURE)
                    self.token_list.append(token)
                elif char == '[':
                    token = Token(char, TokenType.LEFT_BRACKET)
                    self.token_list.append(token)
                elif char == ']':
                    token = Token(char, TokenType.RIGHT_BRACKET)
                    self.token_list.append(token)
                elif char == ':':
                    token = Token(char, TokenType.COLON)
                    self.token_list.append(token)
                else:
                    # Just throw out the character if it's not known!
                    self._consume_char()
            self.pose = 0

    def _tokenize_str_without_quotes(self, line : str):
        char : str = line[self.pose]
        token_val = ""

        while self.pose < len(line) or not char.isspace():
            char = line[self.pose]
            token_val += char
            self._consume_char()

        _require(char, ' ')
        self._consume_char()
        token = Token(token_val, TokenType.STRING)
        self.token_list.append(token)

    def _tokenize_str_with_quotes(self, line : str):
        self._consume_char()
        char : str = line[self.pose]
        token_val = ""

        while self.pose < len(line) or char != '"' or not char.isspace():
            char = line[self.pose]
            token_val += char
            self._consume_char()

        _require(char, '"')
        self._consume_char()
        _require(char, ' ')
        self._consume_char()
        token = Token(token_val, TokenType.STRING)
        self.token_list.append(token)

    def _tokenize_var(self, line : str, token_type : TokenType):
        self._consume_char()
        char : str = line[self.pose]
        token_val = ""

        while self.pose < len(line) or not char.isspace():
            char = line[self.pose]
            token_val += char
            self._consume_char()
        self._consume_char()
        token = Token(token_val, token_type)
        self.token_list.append(token)

    def _consume_char(self):
        self.pose += 1