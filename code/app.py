import math
from queue import Queue
from flask import Flask, request, jsonify
from flask_cors import CORS

from robot_controller import RobotController
from robot import Robot
import threading
from threading import Timer, Thread
import atexit
import time

class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

message_queue = Queue()
server_name = "10.158.167.65"
app = Flask(__name__)
CORS(app)

robot_controller = RobotController(Robot("./testDialogFileForPractice.txt"), 270, 90)

timeout = 5

ping = False

@app.post('/pan_head')
def pan_head():
    if request.is_json:
        data = request.get_json()
        rot = data.get('rot')
        robot_controller.pan_head(int(rot))

        return jsonify({"response": f"Received: {data.get('rot', 'no message')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400


@app.post('/tilt_head')
def tilt_head():
    if request.is_json:
        data = request.get_json()
        rot = data.get('rot')
        robot_controller.tilt_head(int(rot))

        return jsonify({"response": f"Received: {data.get('rot', 'no message')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400



@app.post('/rotate_waist')
def rotate_waist():
    data = request.get_json()
    rot = data.get('rot')
    robot_controller.rotate_waist(int(rot))

    return jsonify({"response": f"Received: {data.get('rot', 'no message')}"}), 200

# Currently this is the only method that is attached to the joystick!
@app.post('/drive')
def drive():
    direction = None

    if request.is_json:
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')

        angle = math.atan2(y,x)
        steering, throttle = calc_servo_speeds(x, y)

        # Stop the wheels no matter what if our website decides it should stop!!!
        if x == 0 and y == 0:
            robot_controller.stop_drive()

        # Here we are turning which shouldn't be affected by blocking!
        if abs(abs(angle) - math.pi/2.0) >= .2:
            robot_controller.turn(int(steering))
            return jsonify({"response": f"Received: {data.get('x', 'no message'), data.get('y', 'no message')}"}), 200
        else: 
        # 6000 is center/neutral, above = forward, below = backward
            if angle < 0:
                direction = "forward"
            elif angle > 0:
                direction = "backward"

            if direction == "forward" and not robot_controller.IsFrontBlocked():
                robot_controller.drive(int(throttle))
            elif direction == "backward" and not robot_controller.IsRearBlocked():
                robot_controller.drive(int(throttle))
            else:
                robot_controller.stop_drive()

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

        if question in ["stop", "cancel", "reset", "quit"]:
            robot_controller.reset_robot_dialog_and_state()

        # Get the question and resolve the response and add that to the message queue
        actions, response = robot_controller.get_dialog_response(question_words)
        print(actions)
        print(response)
        message_queue.put(response)

        if actions:
            robot_controller.queue_actions(actions)

        return jsonify({"response": f"Received: {data.get('question', 'no question')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400


@app.post('/wall_follow')
def wall_follow():
    if request.is_json:
        data = request.get_json()
        do_wall_follow = data.get('state')
        robot_controller.set_do_wall_follow(do_wall_follow)

        if do_wall_follow:
            wall_follow_thread = Thread(target=robot_controller.WallFollowTick)
            wall_follow_thread.start()

        return jsonify({"response": f"Received: {data.get('state', 'no state')}"}), 200
    return jsonify({"error": "Request must be JSON"}), 400

@app.get("/ping")
def fping():
    global ping
    ping = True
    return jsonify({"response": f"Received"}), 200
        
def safety_check():
    global ping
    if(ping):
        ping = False
    elif(not ping):
        print("Connection timeout, stopping drivetrain")
        robot_controller.stop_drive()
    pass

@app.get('/')
def index():
    return 'Hello World!'

def speak_messages():
    global message_queue

    while True:
        if message_queue.qsize() > 0:
            message = message_queue.get()
            robot_controller.speak_message(message)

def main():
    ping = False
    safetythread = RepeatingTimer(timeout, safety_check)
    thread = threading.Thread(target=speak_messages)
    safetythread.start()
    thread.start()

    robot_controller.stop_drive()

    app.config["SERVER_NAME"] = server_name
    app.run(host=server_name, port=5002, debug=True, use_reloader=False)


def exit_handler():
    robot_controller.stop_drive()
    robot_controller.close_robot()
atexit.register(exit_handler)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        robot_controller.stop_drive()
