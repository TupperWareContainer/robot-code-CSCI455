import math
from queue import Queue
from flask import Flask, request, jsonify
from flask_cors import CORS
from robot import Robot
from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser
from al_dialog_program import Program
import threading
import atexit
import time
message_queue = Queue()
server_name = "10.130.187.65"

app = Flask(__name__)
CORS(app)

robot = Robot()

timeout = 2

ping = 0

isPing = False

program : Program

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
        global program
        data = request.get_json()
        question = data.get('question')

        # Get the question and resolve the response and add that to the message queue




        return jsonify({"response": f"Received: {data.get('question', 'no question')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400


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
    path = "./testDialogFileForPractice.txt"
    tokenizer = Tokenizer(path)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens, path)
    program = parser.parse()


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
