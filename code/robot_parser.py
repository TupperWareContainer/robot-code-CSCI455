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
        self.variables = {}  # Store captured variable values

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

            if self.current().get_token_type() == TokenType.DEFINITION:
                self._parse_definition(program)

            elif self.current().get_token_type() == TokenType.LEVEL:
                rule = self._parse_rule()

                # Process dynamic text in pattern and output
                rule.pattern = self._parse_dynamic_text(rule.pattern)
                rule.output = self._parse_dynamic_text(rule.output)

                level_depth = self._level_depth(rule.get_level())

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

        if self.current().get_token_type() != TokenType.LEFT_BRACKET:
            self._parse_str(items)
            return items

        self.expect(TokenType.LEFT_BRACKET)

        while self.current().token_type not in (
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
        item = ""

        while self.current().get_token_type() == TokenType.STRING:
            item = item + self.current().get_value()
            self.advance()
            item = item + " "
        item = item.strip()
        items.append(item)

    def _parse_optional(self, items):
        self.expect(TokenType.LEFT_CURLY)
        items.append(OptionalStr(self.current().get_value()))
        self.advance()
        self.expect(TokenType.RIGHT_CURLY)

    def _parse_dynamic_text(self, tokens_list):
        """Recursively process tokens to handle VAR_CAPTURE (_) and VAR_RECALL ($)."""
        result = []

        for token in tokens_list:
            # If token is a nested list (from nested expressions), recurse
            if isinstance(token, list):
                result.append(self._parse_dynamic_text(token))
                continue

            if isinstance(token, OptionalStr):
                continue

            if token.get_token_type() == TokenType.VAR_CAPTURE:
                # Create a unique placeholder for captured variable
                placeholder_name = f"__var{len(self.variables)}__"
                self.variables[placeholder_name] = None
                result.append(placeholder_name)

            elif token.get_token_type() == TokenType.VAR_RECALL:
                # Insert previously captured variable
                var_name = token.get_name()
                if var_name in self.variables:
                    result.append(self.variables[var_name])
                else:
                    result.append(f"<undefined:{var_name}>")
            else:
                # Regular token, keep its value
                value = token.get_value()
                result.append(value)

        return result