from robot_program import Program
from rule import Rule
from robot_token_type import TokenType
from optional_str import OptionalStr
from robot_token import Token

MAX_DEPTH = 6

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        token = self.current()
        if token.get_token_type() != token_type:
            raise Exception(f"Expected {token_type}, got {token.get_token_type()} with value {token.get_value()}")
        self.advance()
        return token

    def parse(self):
        program = Program()
        rule_stack = []

        while self.current().get_token_type() != TokenType.EOF:
            try:
                if self.current().get_token_type() == TokenType.DEFINITION:
                    self._parse_definition(program)

                elif self.current().get_token_type() == TokenType.LEVEL:
                    rule = self._parse_rule()
                    level_depth = self._level_depth(rule.get_level())

                    # FATAL: missing u level is not allowed
                    if level_depth < 0:
                        raise Exception(f"Fatal error: Invalid rule level '{rule.get_level()}'")

                    # MAX DEPTH GUARD
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
            except Exception as e:
                # Non-fatal error: log and skip the current line
                token = self.current()
                print(f"Warning: {e}. Skipping line starting with token '{token.get_value()}'")
                self._skip_line()

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

        if not level.startswith("u"):
            # fatal: missing 'u'
            raise Exception(f"Rule level '{level}' does not start with 'u'")

        self.expect(TokenType.COLON)

        self.expect(TokenType.LEFT_PAREN)

        if self.current().get_token_type() == TokenType.DEFINITION:
            pattern = self.current()
            self.advance()
        else:
            pattern = self._parse_expression()

        self.expect(TokenType.RIGHT_PAREN)
        self.expect(TokenType.COLON)

        if self.current().get_token_type() == TokenType.DEFINITION:
            output = self.current()
            self.advance()
        else:
            output = self._parse_expression()

        actions = []
        while self.current().get_token_type() == TokenType.ACTION:
            actions.append(self.current())
            self.advance()

        rule = Rule(level, pattern, output)
        rule.set_actions(actions)
        return rule

    def _parse_expression(self):
        items = []

        if self.current().get_token_type() != TokenType.LEFT_BRACKET:
            self._parse_str(items)
            return items

        self.expect(TokenType.LEFT_BRACKET)

        while self.current().get_token_type() not in (
            TokenType.NEWLINE,
            TokenType.RIGHT_PAREN,
            TokenType.EOF,
            TokenType.RIGHT_BRACKET
        ):
            if self.current().get_token_type() == TokenType.LEFT_CURLY:
                self._parse_optional(items)
            elif self.current().get_token_type() == TokenType.VAR_CAPTURE:
                items.append(self.current())
                self.advance()
            elif self.current().get_token_type() == TokenType.VAR_RECALL:
                items.append(self.current())
                self.advance()
            else:
                items.append(self.current())
                self.advance()

        self.expect(TokenType.RIGHT_BRACKET)

        return items

    def _parse_str(self, items):
        while (self.current().get_token_type() == TokenType.STRING
               or self.current().get_token_type() == TokenType.VAR_CAPTURE
               or self.current().get_token_type() == TokenType.VAR_RECALL):
            items.append(self.current())
            self.advance()

    def _parse_optional(self, items):
        self.expect(TokenType.LEFT_CURLY)

        optional_tokens = []

        while self.current().get_token_type() != TokenType.RIGHT_CURLY:
            optional_tokens.append(self.current())
            self.advance()

        self.expect(TokenType.RIGHT_CURLY)
        items.append(OptionalStr(optional_tokens))

    def _skip_line(self):
        while self.current().get_token_type() not in (TokenType.NEWLINE, TokenType.EOF):
            self.advance()
        if self.current().get_token_type() == TokenType.NEWLINE:
            self.advance()