from token_type import TokenType
from token import Token

def _is_whitespace(char):
    return char == ' ' or char == '\t'

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
                char = line[self.pose]

                if char == '#' or not line:
                    continue
                elif char == '"':
                    self._tokenize_str(line)
                elif char == '&':
                    self._tokenize_var(line)
                else:
                    # Just throw out the character if it's not known!
                    self._consume_char()
            self.pose = 0

    def _tokenize_str(self, line):
        self._consume_char()
        char = line[self.pose]
        token_val = ""

        while self.pose < line or char != '"' or not _is_whitespace(char):
            char = line[self.pose]
            token_val += char
            self._consume_char()

        self._require(char, '"')
        self._require(char, ' ')
        token = Token(token_val, TokenType.STRING)
        self.token_list.append(token)

    def _tokenize_var(self, line):
        self._consume_char()
        char = line[self.pose]
        token = ""

        while self.pose < line or not _is_whitespace(char):
            char = line[self.pose]
            token += char
            self._consume_char()

    def _consume_char(self):
        self.pose += 1

    def _require(self, char, required_char):
        if char != required_char:
            print("Error: Invalid character expected:", required_char)
            return False
        return True