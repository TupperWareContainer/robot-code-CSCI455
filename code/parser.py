from program import Program
from rule import Rule
from token_type import TokenType

MAX_DEPTH = 6

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        token = self.current()
        if token.get_token_type() != token_type:
            raise Exception(f"Expected {token_type}, got {token.get_token_type()}")
        self.advance()
        return token

    def parse(self):
        program = Program()
        rule_stack = []

        while self.current().get_token_type() != TokenType.EOF:

            if self.current().get_token_type() == TokenType.DEFINITION:
                self._parse_definition(program)

            elif self.current().get_token_type() == TokenType.LEVEL:
                rule = self._parse_rule()

                level_depth = self._level_depth(rule.get_level())

                # -----------------------------
                # MAX DEPTH GUARD
                # -----------------------------
                if level_depth > MAX_DEPTH:
                    print(
                        f"Error: Rule depth {level_depth} exceeds max depth {MAX_DEPTH}. "
                        f"Rule '{rule.get_level()}' ignored."
                    )
                    continue

                # adjust stack to correct depth
                while len(rule_stack) > level_depth:
                    rule_stack.pop()

                if rule_stack:
                    rule_stack[-1].children.append(rule)
                else:
                    program.rules.append(rule)

                rule_stack.append(rule)

            else:
                self.advance()

        return program

    def _level_depth(self, level_token):
        if level_token == "u":
            return 0

        try:
            return int(level_token[1:])
        except ValueError:
            print(f"Invalid level format: {level_token}")
            return -1

    def _parse_definition(self, program):
        name = self.current().value
        self.advance()
        self.expect(TokenType.COLON)

        choices = self._parse_expression()
        program.add_definition(name, choices)

    def _parse_rule(self):
        level = self.current().value
        self.advance()
        self.expect(TokenType.COLON)
        self.expect(TokenType.LEFT_PAREN)

        pattern = self._parse_expression()

        self.expect(TokenType.RIGHT_PAREN)
        self.expect(TokenType.COLON)

        output = self._parse_expression()

        return Rule(level, pattern, output)

    def _parse_expression(self):
        items = []

        while self.current().token_type not in (
            TokenType.NEWLINE,
            TokenType.RIGHT_PAREN,
            TokenType.EOF
        ):
            items.append(self.current())
            self.advance()

        return items