from token import Token
from token_type import TokenType

class Tokenizer:
    class Tokenizer:

        def __init__(self, file_path):
            self.file_path = file_path
            self.tokens = []

        def parse(self):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    self._tokenize_line(line)

            self.tokens.append(Token("", TokenType.EOF))

        def _tokenize_line(self, line):
            # Ignore full-line comments
            if line.strip().startswith("#"):
                return

            line = line.strip()
            pos = 0

            while pos < len(line):
                char = line[pos]

                if char.isspace():
                    pos += 1

                elif char == '(':
                    self.tokens.append(Token("(", TokenType.LEFT_PAREN))
                    pos += 1

                elif char == ')':
                    self.tokens.append(Token(")", TokenType.RIGHT_PAREN))
                    pos += 1

                elif char == '[':
                    self.tokens.append(Token("[", TokenType.LEFT_BRACKET))
                    pos += 1

                elif char == ']':
                    self.tokens.append(Token("]", TokenType.RIGHT_BRACKET))
                    pos += 1

                elif char == ':':
                    self.tokens.append(Token(":", TokenType.COLON))
                    pos += 1

                elif char == '<':
                    pos += 1
                    start = pos
                    while pos < len(line) and line[pos] != '>':
                        pos += 1
                    value = line[start:pos]
                    self.tokens.append(Token(value, TokenType.ACTION))
                    pos += 1  # skip '>'

                elif char == '"':
                    pos += 1
                    start = pos
                    while pos < len(line) and line[pos] != '"':
                        pos += 1
                    value = line[start:pos]
                    self.tokens.append(Token(value, TokenType.STRING))
                    pos += 1  # skip closing quote

                elif char == '~':
                    pos += 1
                    start = pos
                    while pos < len(line) and line[pos].isalnum():
                        pos += 1
                    value = line[start:pos]
                    self.tokens.append(Token(value, TokenType.DEFINITION))

                elif char == '&':
                    pos += 1
                    start = pos
                    while pos < len(line) and line[pos].isalnum():
                        pos += 1
                    value = line[start:pos]
                    self.tokens.append(Token(value, TokenType.VAR))

                elif char == '$':
                    pos += 1
                    start = pos
                    while pos < len(line) and line[pos].isalnum():
                        pos += 1
                    value = line[start:pos]
                    self.tokens.append(Token(value, TokenType.VAR_RECALL))

                elif char == '_':
                    self.tokens.append(Token("_", TokenType.VAR_CAPTURE))
                    pos += 1

                elif char.isalnum():
                    start = pos
                    while pos < len(line) and line[pos].isalnum():
                        pos += 1
                    value = line[start:pos]

                    if (value.startswith("u") and value[1:].isdigit()) or value == "u":
                        self.tokens.append(Token(value, TokenType.LEVEL))
                    else:
                        self.tokens.append(Token(value, TokenType.STRING))

                else:
                    # Skip unknown characters
                    pos += 1

            self.tokens.append(Token("", TokenType.NEWLINE))