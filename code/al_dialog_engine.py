from al_dialog_choice import Choice
from al_dialog_token import Token
from al_dialog_token_type import TokenType
from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser

from collections import deque

class AlDialogEngine:
    def __init__(self, path : str):
        self.rules: deque = deque()
        self.program = self.parse_program(path)

    def parse_program(self, path):
        tokenizer = Tokenizer(path)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens, path)
        program = parser.parse()
        self.rules.appendleft(program.get_rules())
        return program

    def reset_dialog(self):
        self.rules.clear()
        self.rules.appendleft(self.program.get_rules())

    def get_response(self, question_words) -> tuple[list, str]:
        if not question_words:
            return [], "I don't know that"

        definitions = self.program.get_definitions()

        top_rules = self.rules[0]
        user_vars, rule = self._find_rule(definitions, top_rules, question_words)

        if rule is not None:
            # If the rule has children go down one level!
            if rule.get_children():
                self.rules.appendleft(rule.get_children())

            return self._process_output(rule, user_vars, definitions)
        else:
            # If there is no outer scope then we need to return early!
            if len(self.rules) <= 1:
                return [], "I don't know that"

            # Peak at the next outer scope to try to find the rule there!
            next_rules = self.rules[1]
            user_vars, rule = self._find_rule(definitions, next_rules, question_words)

            if rule is None:
                return [], "I don't know that"
            else:
                self.rules.popleft()
                return self._process_output(rule, user_vars, definitions)

    def _process_output(self, rule, user_vars, definitions) -> tuple[list, str]:
        response: list = []

        if rule is None:
            return [], "I don't know that"

        if rule is not None:
            output = rule.get_output()

            if isinstance(output, Token):
                if output.get_token_type() == TokenType.DEFINITION:
                    value = output.get_value()

                    definition = definitions.get(value, [])
                    choices = definition.get_choices()[0]
                    token = choices.get_random()
                    # Rewrap the token in a list to prevent a crash!
                    output = [token]
                else:
                    token = output
                    # Rewrap the token in a list to prevent a crash!
                    output = [token]

            for token in output:
                if isinstance(token, Choice):
                    # If there is a choice we first need to pick a random one!
                    token = token.get_random()

                token_type = token.get_token_type()
                value = token.get_value()

                if token_type == TokenType.VAR_RECALL:
                    if not user_vars:
                        response.append(self.program.get_user_var(value, "I don't know"))
                    else:
                        self.program.add_user_var(value, user_vars[0])
                        response.append(user_vars[0])
                        user_vars.pop(0)
                else:
                    response.append(value)
            return rule.get_actions(), " ".join(response)

        return [], "I don't know that"

    def _find_rule(self, definitions, current_rules, question_words):
        rules_sorted = sorted(current_rules, key=lambda r: r.get_level())

        for rule in rules_sorted:
            matched, vars_found, matched_rule = self._search_rule(
                rule,
                definitions,
                question_words
            )

            if matched:
                return vars_found, matched_rule

        return [], None

    def _search_rule(self, rule, definitions, question_words):
        pattern = rule.get_pattern()

        if not isinstance(pattern, list):
            pattern = [pattern]

        matched, vars_found = self._match_pattern(
            pattern,
            definitions,
            question_words
        )

        if matched:
            return True, vars_found, rule

        return False, [], None

    def _match_pattern(self, pattern, definitions, question_words):
        user_vars = []
        i = 0

        for element in pattern:

            matched, captured, consumed = self._match_element(
                element,
                question_words,
                i,
                definitions
            )

            if not matched:
                return False, []

            if captured is not None:
                user_vars.append(captured)

            i += consumed

        # Ensure full sentence matched
        if i != len(question_words):
            return False, []

        return True, user_vars

    def _match_element(self, element, question_words, start_index, definitions):
        # Choice object
        if isinstance(element, Choice):

            for token in element.get_choices():
                matched, captured, consumed = self._match_token(token, question_words, start_index, definitions)

                if matched:
                    return True, captured, consumed

            return False, None, 0

        # Normal token
        return self._match_token(element, question_words, start_index, definitions)

    def _match_token(self, token, question_words, start_index, definitions):
        token_type = token.get_token_type()
        value = token.get_value()

        if token_type == TokenType.VAR_CAPTURE:
            captured_value = question_words[start_index]
            return True, captured_value, 1

        if token_type == TokenType.DEFINITION:
            choices: Choice = definitions.get(value, []).get_choices()[0]

            if choices.contains_choice(start_index, question_words):
                # The full word has been matched!
                consumed = len(question_words) - start_index
                return True, None, consumed
            return False, None, 0

        if token_type == TokenType.OPTIONAL:
            return True, None, 0

        if token_type == TokenType.STRING:
            token_words = value.split()  # "hi there" → ["hi", "there"]
            end = start_index + len(token_words)

            if end > len(question_words):
                return False, None, 0

            if question_words[start_index:end] == token_words:
                return True, None, len(token_words)  # consume all words
            return False, None, 0

        if start_index < len(question_words):
            return question_words[start_index] == value, None, 1
        return False, None, len(question_words) - start_index