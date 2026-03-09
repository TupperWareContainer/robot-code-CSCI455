from al_dialog_token import Token
from al_dialog_token_type import TokenType
import string


class Tokenizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = []

    def tokenize(self):
        """
            This method is used to tokenize an ALDialog file's contents.
            :return: list: A list of tokens from the file!
        """

        with open(self.file_path, 'r', encoding='utf-8') as file:
            line_num : int = 1

            for line in file:
                self._tokenize_line(line, line_num)
                line_num += 1

        self.tokens.append(Token("", TokenType.EOF, line_num))
        return self.tokens

    def _tokenize_line(self, line, line_num):
        # Ignore full-line comments
        if line.strip().startswith("#"):
            return

        line = line.strip().lower()
        translator = str.maketrans('', '', string.punctuation)
        line = line.translate(translator)
        pos = 0

        while pos < len(line):
            char = line[pos]

            if char.isspace():
                pos += 1

            elif char == '(':
                self.tokens.append(Token("(", TokenType.LEFT_PAREN, line_num))
                pos += 1

            elif char == '{':
                pos += 1
                start = pos
                while pos < len(line) and line[pos] != '}':
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.OPTIONAL, line_num))
                pos += 1  # skip closing curly

            elif char == ')':
                self.tokens.append(Token(")", TokenType.RIGHT_PAREN, line_num))
                pos += 1

            elif char == '[':
                self.tokens.append(Token("[", TokenType.LEFT_BRACKET, line_num))
                pos += 1

            elif char == ']':
                self.tokens.append(Token("]", TokenType.RIGHT_BRACKET, line_num))
                pos += 1

            elif char == ':':
                self.tokens.append(Token(":", TokenType.COLON, line_num))
                pos += 1

            elif char == '<':
                pos += 1
                start = pos
                while pos < len(line) and line[pos] != '>':
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.ACTION, line_num))
                pos += 1  # skip '>'

            elif char == '"':
                pos += 1
                start = pos
                while pos < len(line) and line[pos] != '"':
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.STRING, line_num))
                pos += 1  # skip closing quote

            elif char == '~':
                pos += 1
                start = pos
                while pos < len(line) and (line[pos].isalnum() or line[pos] == '_'):
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.DEFINITION, line_num))

            elif char == '&':
                pos += 1
                start = pos
                while pos < len(line) and (line[pos].isalnum() or line[pos] == '_'):
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.VAR, line_num))

            elif char == '$':
                pos += 1
                start = pos
                while pos < len(line) and (line[pos].isalnum() or line[pos] == '_'):
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.VAR_RECALL, line_num))

            elif char == '_':
                self.tokens.append(Token("_", TokenType.VAR_CAPTURE, line_num))
                pos += 1

            elif char.isalnum():
                start = pos
                while pos < len(line) and line[pos].isalnum():
                    pos += 1
                value = line[start:pos]

                if (value.startswith("u") and value[1:].isdigit()) or value == "u":
                    self.tokens.append(Token(value, TokenType.LEVEL, line_num))
                else:
                    self.tokens.append(Token(value, TokenType.STRING, line_num))

            else:
                # Skip unknown characters
                pos += 1

        self.tokens.append(Token("", TokenType.NEWLINE, line_num))
