from token import Token
from token_type import TokenType

class Tokenizer:

    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = []
        self.indent_stack = [0]

    def parse(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                self._tokenize_line(line)

        # close remaining indents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token("", TokenType.DEDENT))

        self.tokens.append(Token("", TokenType.EOF))

    def _tokenize_line(self, line):
        if line.strip().startswith("#"):
            return

        indent = len(line) - len(line.lstrip(" "))
        self._handle_indent(indent)

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
                start = pos + 1
                pos += 1
                while pos < len(line) and line[pos] != '>':
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.ACTION))
                pos += 1

            elif char == '"':
                start = pos + 1
                pos += 1
                while pos < len(line) and line[pos] != '"':
                    pos += 1
                value = line[start:pos]
                self.tokens.append(Token(value, TokenType.STRING))
                pos += 1

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
                while pos < len(line) and not line[pos].isspace():
                    pos += 1
                value = line[start:pos]

                if value.startswith("u") and value[1:].isdigit() or value == "u":
                    self.tokens.append(Token(value, TokenType.LEVEL))
                else:
                    self.tokens.append(Token(value, TokenType.STRING))

            else:
                pos += 1

        self.tokens.append(Token("", TokenType.NEWLINE))

    def _handle_indent(self, indent):
        if indent > self.indent_stack[-1]:
            self.indent_stack.append(indent)
            self.tokens.append(Token("", TokenType.INDENT))
        else:
            while indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token("", TokenType.DEDENT))