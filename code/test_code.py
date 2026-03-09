import string

from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser
from al_dialog_program import Program
from al_dialog_token_type import TokenType
from al_dialog_choice import Choice

program : Program

def parse_program():
    global program
    path = "./testDialogFileForPractice.txt"
    tokenizer = Tokenizer(path)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens, path)
    program = parser.parse()

def main():
    parse_program()
    global program
    question: str = "hi there."
    translator = str.maketrans('', '', string.punctuation)
    question = question.translate(translator)
    question_words = question.split()

    # Get the question and resolve the response and add that to the message queue
    response = get_response(question_words)
    print(response)


def get_response(question_words):
    global program
    rules = program.get_rules()
    definitions = program.get_definitions()
    response : list = []

    user_vars, rule = find_rule(definitions, rules, question_words)

    if rule is not None:
        output = rule.get_output()

        for token in output:
            token_type = token.get_token_type()
            value = token.get_value()

            if token_type == TokenType.VAR_RECALL:
                if user_vars:
                    program.add_user_var(value, user_vars[0])
                    user_vars.pop(0)
                else:
                    response.append("I don't know")
            else:
                response.append(value)

    return " ".join(response)

def find_rule(definitions, rules, question_words):

    rules_sorted = sorted(rules, key=lambda r: r.get_level())

    for rule in rules_sorted:
        matched, vars_found, matched_rule = search_rule(
            rule,
            definitions,
            question_words
        )

        if matched:
            return vars_found, matched_rule

    return [], None

def search_rule(rule, definitions, question_words):

    pattern = rule.get_pattern()

    if not isinstance(pattern, list):
        pattern = [pattern]

    matched, vars_found = match_pattern(
        pattern,
        definitions,
        question_words
    )

    if not matched:
        return False, [], None

    # search children
    for child in rule.get_children():
        child_match, child_vars, child_rule = search_rule(
            child,
            definitions,
            question_words
        )

        if child_match:
            return True, vars_found + child_vars, child_rule

    return True, vars_found, rule

def match_pattern(pattern, definitions, question_words):

    if len(question_words) < len(pattern):
        return False, []

    user_vars = []

    for i, element in enumerate(pattern):

        word = question_words[i]

        matched, captured = match_element(
            element,
            word,
            definitions
        )

        if not matched:
            return False, []

        if captured is not None:
            user_vars.append(captured)

    return True, user_vars

def match_element(element, word, definitions):

    # Choice object
    if isinstance(element, Choice):

        for token in element.get_choices():

            matched, captured = match_token(
                token,
                word,
                definitions
            )

            if matched:
                return True, captured

        return False, None

    # Normal token
    return match_token(element, word, definitions)

def match_token(token, word, definitions):

    token_type = token.get_token_type()
    value = token.get_value()

    if token_type == TokenType.VAR_CAPTURE:
        return True, word

    if token_type == TokenType.DEFINITION:
        choices = definitions.get(value, [])
        return word in choices, None

    if token_type == TokenType.OPTIONAL:
        return True, None

    return word == value, None

if __name__ == '__main__':
    main()