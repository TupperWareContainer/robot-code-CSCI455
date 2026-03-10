import string

from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser
from al_dialog_program import Program
from al_dialog_rule import Rule

program : Program
rules : Rule

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
    global rules
    rules = program.get_rules()
    question: str = "My name is ryan"
    question2 : str = "What is my name"
    question3 : str = "let us talk"
    question4 : str = "are you happy"

    translator = str.maketrans('', '', string.punctuation)
    question = question.translate(translator)
    question_words = question.lower().split()
    question2_words = question2.lower().split()
    question3_words = question3.lower().split()
    question4_words = question4.lower().split()


# def get_response(question_words):
#     global program
#     global rules
#
#     definitions = program.get_definitions()
#     response : list = []
#
#     user_vars, rule = find_rule(definitions, rules, question_words)
#
#     if rule.get_children():
#         rules = rule.get_children()
#
#     if rule is not None:
#         output = rule.get_output()
#
#         if isinstance(output, Token):
#             if output.get_token_type() == TokenType.DEFINITION:
#                 value = output.get_value()
#
#                 definition = definitions.get(value, [])
#                 choices = definition.get_choices()[0]
#                 output = choices.get_random()
#
#         for token in output:
#             if isinstance(token, Choice):
#                 # If there is a choice we first need to pick a random one!
#                 token = token.get_random()
#
#             token_type = token.get_token_type()
#             value = token.get_value()
#
#             if token_type == TokenType.VAR_RECALL:
#                 if not user_vars:
#                     response.append(program.get_user_var(value, "I don't know"))
#                 else:
#                     program.add_user_var(value, user_vars[0])
#                     response.append(user_vars[0])
#                     user_vars.pop(0)
#             else:
#                 response.append(value)
#         return " ".join(response)
#     else:
#         return "I don't know that"
#
#
# def find_rule(definitions, rules, question_words):
#     rules_sorted = sorted(rules, key=lambda r: r.get_level())
#
#     for rule in rules_sorted:
#         matched, vars_found, matched_rule = search_rule(
#             rule,
#             definitions,
#             question_words
#         )
#
#         if matched:
#             return vars_found, matched_rule
#
#     return [], None
#
# def search_rule(rule, definitions, question_words):
#     pattern = rule.get_pattern()
#
#     if not isinstance(pattern, list):
#         pattern = [pattern]
#
#     matched, vars_found = match_pattern(
#         pattern,
#         definitions,
#         question_words
#     )
#
#     if not matched:
#         return False, [], None
#
#     # search children
#     for child in rule.get_children():
#         child_match, child_vars, child_rule = search_rule(
#             child,
#             definitions,
#             question_words
#         )
#
#         if child_match:
#             return True, vars_found + child_vars, child_rule
#
#     return True, vars_found, rule
#
# def match_pattern(pattern, definitions, question_words):
#     user_vars = []
#     i = 0
#
#     for element in pattern:
#
#         matched, captured, consumed = match_element(
#             element,
#             question_words,
#             i,
#             definitions
#         )
#
#         if not matched:
#             return False, []
#
#         if captured is not None:
#             user_vars.append(captured)
#
#         i += consumed
#
#     # Ensure full sentence matched
#     if i != len(question_words):
#         return False, []
#
#     return True, user_vars
#
# def match_element(element, question_words, start_index, definitions):
#
#     # Choice object
#     if isinstance(element, Choice):
#
#         for token in element.get_choices():
#             matched, captured, consumed = match_token(token, question_words, start_index, definitions)
#
#             if matched:
#                 return True, captured, consumed
#
#         return False, None, 0
#
#     # Normal token
#     return match_token(element, question_words, start_index, definitions)
#
# def match_token(token, question_words, start_index, definitions):
#     token_type = token.get_token_type()
#     value = token.get_value()
#
#     if token_type == TokenType.VAR_CAPTURE:
#         captured_value = question_words[start_index]
#         return True, captured_value, 1
#
#     if token_type == TokenType.DEFINITION:
#         choices : Choice = definitions.get(value, []).get_choices()[0]
#
#         if choices.contains_choice(start_index, question_words):
#             # The full word has been matched!
#             consumed = len(question_words) - start_index
#             return True, None, consumed
#         return False, None, 0
#
#     if token_type == TokenType.OPTIONAL:
#         return True, None, 0
#
#     return question_words[start_index] == value, None, 1

if __name__ == '__main__':
    main()