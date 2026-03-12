import math
from queue import Queue
from flask import Flask, request, jsonify
from flask_cors import CORS
from robot import Robot
from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser
from al_dialog_program import Program
from al_dialog_token_type import TokenType
from al_dialog_token import Token
from al_dialog_choice import Choice
from robotcontroller import RobotController
from collections import deque
import threading
import atexit
import time
message_queue = Queue()
server_name = "10.23.253.65"

app = Flask(__name__)
CORS(app)

robot = Robot()

timeout = 2

ping = 0

isPing = False

program : Program
rules : deque = deque()
controller : RobotController

@app.post('/pan_head')
def pan_head():
    if request.is_json:
        data = request.get_json()
        rot = data.get('rot')
        robot.pan_head(int(rot))

        return jsonify({"response": f"Received: {data.get('rot', 'no message')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400


@app.post('/tilt_head')
def tilt_head():
    if request.is_json:
        data = request.get_json()
        rot = data.get('rot')
        robot.tilt_head(int(rot))

        return jsonify({"response": f"Received: {data.get('rot', 'no message')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400



@app.post('/rotate_waist')
def rotate_waist():
    robot = Robot()


    data = request.get_json()
    rot = data.get('rot')
    robot.rotate_waist(int(rot))

    return jsonify({"response": f"Received: {data.get('rot', 'no message')}"}), 200

# Currently this is the only method that is attached to the joystick!
@app.post('/drive')
def drive():
    if request.is_json:
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        
        steering, throttle = calc_servo_speeds(x, y)
        print(steering)
        print(throttle)

        if(abs(x) > abs(y)):
            robot.drive_wheels(int(throttle))
        elif(abs(y) > abs(x)):
           robot.turn_wheels(int(steering))
        elif(steering == throttle == 6000):
            robot.turn_wheels(int(steering))
            robot.drive_wheels(int(throttle))
        return jsonify({"response": f"Received: {data.get('x', 'no message'), data.get('y', 'no message')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400

def calc_servo_speeds(joystick_x, joystick_y):
    angle = math.atan2(joystick_y, joystick_x)
    force_magnitude = math.sqrt((joystick_x ** 2) + (joystick_y ** 2))

    x_norm = math.cos(angle) * force_magnitude
    y_norm = math.sin(angle) * force_magnitude

    x = round(x_norm * 2000 + 6000)
    y = round(y_norm * 2000 + 6000)

    x = max(4000, min(8000, x))
    y = max(4000, min(8000, y))

    steering = x
    throttle = y

    return steering, throttle


@app.post('/speak')
def speak():
    if request.is_json:
        data = request.get_json()
        message = data.get('message')
        message_queue.put(message)
        print(message)

        return jsonify({"response": f"Received: {data.get('message', 'no message')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400


@app.post('/ask')
def ask():
    if request.is_json:
        data = request.get_json()
        question : str = data.get('question')
        translator = str.maketrans('', '', ".,?!'")
        question = question.translate(translator)
        question_words = question.lower().split()

        # Get the question and resolve the response and add that to the message queue
        actions, response = get_response(question_words)
        print(actions)
        print(response)
        message_queue.put(response)

        if question in ["stop", "cancel", "reset", "quit"]:
            stop()

        if actions:
            queue_actions(actions)

        return jsonify({"response": f"Received: {data.get('question', 'no question')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400

def queue_actions(actions):
    global controller

    for action in actions:
        action_value = action.get_value()
        controller.AddActionViaStr(action_value)

def stop():
    global program
    global rules
    global controller

    controller.Reset()
    rules.clear()
    rules.appendleft(program.get_rules())

def get_response(question_words) -> tuple[list, str]:
    global program
    global rules

    if not question_words:
        return [], "I don't know that"

    definitions = program.get_definitions()

    top_rules = rules[0]
    user_vars, rule = find_rule(definitions, top_rules, question_words)

    if rule is not None:
        # If the rule has children go down one level!
        if rule.get_children():
            rules.appendleft(rule.get_children())

        return process_output(rule, user_vars, definitions)
    else:
        # If there is no outer scope then we need to return early!
        if len(rules) <= 1:
            return [], "I don't know that"

        # Peak at the next outer scope to try to find the rule there!
        next_rules = rules[1]
        user_vars, rule = find_rule(definitions, next_rules, question_words)

        if rule is None:
            return [], "I don't know that"
        else:
            rules.popleft()
            return process_output(rule, user_vars, definitions)

def process_output(rule, user_vars, definitions) -> tuple[list, str]:
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
                    response.append(program.get_user_var(value, "I don't know"))
                else:
                    program.add_user_var(value, user_vars[0])
                    response.append(user_vars[0])
                    user_vars.pop(0)
            else:
                response.append(value)
        return rule.get_actions(), " ".join(response)

    return [], "I don't know that"


def find_rule(definitions, current_rules, question_words):
    rules_sorted = sorted(current_rules, key=lambda r: r.get_level())

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

    if matched:
        return True, vars_found, rule

    return False, [], None

def match_pattern(pattern, definitions, question_words):
    user_vars = []
    i = 0

    for element in pattern:

        matched, captured, consumed = match_element(
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

def match_element(element, question_words, start_index, definitions):

    # Choice object
    if isinstance(element, Choice):

        for token in element.get_choices():
            matched, captured, consumed = match_token(token, question_words, start_index, definitions)

            if matched:
                return True, captured, consumed

        return False, None, 0

    # Normal token
    return match_token(element, question_words, start_index, definitions)

def match_token(token, question_words, start_index, definitions):
    token_type = token.get_token_type()
    value = token.get_value()

    if token_type == TokenType.VAR_CAPTURE:
        captured_value = question_words[start_index]
        return True, captured_value, 1

    if token_type == TokenType.DEFINITION:
        choices : Choice = definitions.get(value, []).get_choices()[0]

        if choices.contains_choice(start_index, question_words):
            # The full word has been matched!
            consumed = len(question_words) - start_index
            return True, None, consumed
        return False, None, 0

    if token_type == TokenType.OPTIONAL:
        return True, None, 0

    return question_words[start_index] == value, None, 1

@app.get("/ping")
def fping():
    global ping
    ping = time.time()
    return jsonify({"response": f"Received"}), 200
        
def safety_check():
    global ping
    while(True):
        cTime = time.time()
        if( (cTime - ping) > timeout):
            print("Connection Lost, deactivating drivetrain")
            tempstop()
        time.sleep(1)

def parse_program():
    global program
    global rules
    path = "./testDialogFileForPractice.txt"
    tokenizer = Tokenizer(path)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens, path)
    program = parser.parse()
    rules.appendleft(program.get_rules())


@app.get('/')
def index():
    return 'Hello World!'

def speak_messages():
    global message_queue

    while True:
        if message_queue.qsize() > 0:
            message = message_queue.get()
            robot.speak(message)


def main():
    parse_program()
    safetythread = threading.Thread(target=safety_check)
    thread = threading.Thread(target=speak_messages)
    safetythread.start()
    thread.start()

    robot.drive_wheels(6000)
    app.config["SERVER_NAME"] = server_name
    app.run(host=server_name, port=5002, debug=True)

def tempstop():
    robot.drive_wheels(6000)
    robot.turn_wheels(6000)


def exit_handler():
    robot.drive_wheels(6000)
    robot.turn_wheels(6000)
    robot.close()
atexit.register(exit_handler)


if __name__ == '__main__':
    main()
