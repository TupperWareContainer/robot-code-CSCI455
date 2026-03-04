import os

from al_dialog_program import Program
from al_dialog_rule import Rule
from al_dialog_token_type import TokenType
from al_dialog_optional_str import OptionalStr
from al_dialog_token import Token

MAX_DEPTH = 6

class Parser:

    def __init__(self, tokens, path):
        self.tokens = tokens
        self.pos = 0
        self.file_name = os.path.basename(path)

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self):
        self.pos += 1

    def _expect(self, token_type):
        token = self._current()
        if token.get_token_type() != token_type:
            raise Exception(f"Expected {token_type}, got {token.get_token_type()} with value '{token.get_value()}'")
        self._advance()
        return token

    def parse(self):
        """
            This method parses the token list from an ALDialog file that is passed in when the Parser is created.

            :return: program: This is an object-oriented representation of the tokens that has been parsed!
            The parser keeps the original tokens that were passed!
        """

        program = Program()
        rule_stack = []

        while self._current().get_token_type() != TokenType.EOF:
            try:
                if self._current().get_token_type() == TokenType.DEFINITION:
                    self._parse_definition(program)

                elif self._current().get_token_type() == TokenType.LEVEL:
                    rule = self._parse_rule()
                    level_depth = self._level_depth(rule.get_level())

                    # FATAL: missing u level is not allowed
                    if level_depth < 0:
                        raise Exception(f"Fatal Error: Invalid rule level '{rule.get_level()}'")

                    # MAX DEPTH GUARD
                    if level_depth > MAX_DEPTH:
                        token = self._current()
                        print(
                            f"Non-fatal Error: Rule depth {level_depth} exceeds max depth {MAX_DEPTH}. "
                            f"Rule '{rule.get_level()}' ignored. In file {self.file_name}, skipping line {token.get_line_num()}"
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
                    self._advance()
            except Exception as e:
                # Non-fatal error: log and skip the current line
                token = self._current()
                print(f"Non-fatal Error: {str(e)}, file name: {self.file_name}, skipping line {token.get_line_num()}")
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
        name = self._current().value
        self._advance()
        self._expect(TokenType.COLON)

        choices = self._parse_expression()
        program.add_definition(name, choices)

    def _parse_rule(self):
        level = self._current().value
        self._advance()

        if not level.startswith("u"):
            # fatal: missing 'u'
            token = self._current()
            raise Exception(f"Fatal: Rule level '{level}' does not start with 'u' "
                            f"in file {self.file_name} at line {token.get_line_num()}")

        self._expect(TokenType.COLON)
        self._expect(TokenType.LEFT_PAREN)

        # Pattern can be a definition token or expression
        if self._current().get_token_type() == TokenType.DEFINITION:
            pattern = self._current()
            self._advance()
        else:
            pattern = self._parse_expression()

        self._expect(TokenType.RIGHT_PAREN)
        self._expect(TokenType.COLON)

        # Output can be a definition token or expression
        if self._current().get_token_type() == TokenType.DEFINITION:
            output = self._current()
            self._advance()
        else:
            output = self._parse_expression()

        # Collect multiple action tokens
        actions = []
        while self._current().get_token_type() == TokenType.ACTION:
            actions.append(self._current())
            self._advance()

        rule = Rule(level, pattern, output)
        rule.set_actions(actions)
        return rule

    def _parse_expression(self):
        items = []

        if self._current().get_token_type() != TokenType.LEFT_BRACKET:
            self._parse_str(items)
            return items

        self._expect(TokenType.LEFT_BRACKET)

        while self._current().get_token_type() not in (
            TokenType.NEWLINE,
            TokenType.RIGHT_PAREN,
            TokenType.EOF,
            TokenType.RIGHT_BRACKET
        ):
            if self._current().get_token_type() == TokenType.LEFT_CURLY:
                self._parse_optional(items)
            elif self._current().get_token_type() == TokenType.VAR_CAPTURE:
                items.append(self._current())
                self._advance()
            elif self._current().get_token_type() == TokenType.VAR_RECALL:
                items.append(self._current())
                self._advance()
            else:
                items.append(self._current())
                self._advance()

        self._expect(TokenType.RIGHT_BRACKET)

        return items

    def _parse_str(self, items):
        while self._current().get_token_type() in (TokenType.STRING,
                                                   TokenType.VAR_CAPTURE,
                                                   TokenType.VAR_RECALL):
            items.append(self._current())
            self._advance()

    def _parse_optional(self, items):
        self._expect(TokenType.LEFT_CURLY)

        optional_tokens = []

        while self._current().get_token_type() != TokenType.RIGHT_CURLY:
            optional_tokens.append(self._current())
            self._advance()

        self._expect(TokenType.RIGHT_CURLY)
        items.append(OptionalStr(optional_tokens))

    def _skip_line(self):
        while self._current().get_token_type() not in (TokenType.NEWLINE, TokenType.EOF):
            self._advance()
        if self._current().get_token_type() == TokenType.NEWLINE:
            self._advance()