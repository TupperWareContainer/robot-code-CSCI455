from robot_controller import RobotController
from head_controller import HeadController
from waist_controller import WaistController
from wheel_controller import WheelController
from arm_controller import ArmController
from voice import Voice
from espeakng import ESpeakNG
from al_dialog_engine import AlDialogEngine
import maestro

class Robot:
    master_controller : maestro.Controller
    espeak  : ESpeakNG
    head    : HeadController
    wheels  : WheelController
    waist   : WaistController
    arm     : ArmController
    voice   : Voice
    robot_controller : RobotController
    __MOTORCHANNELS = [3,4,5,0,1,6]

    def __init__(self, speech_engine_path):
        # Add the logic for tty1 vs tty0 here
        self.master_controller = maestro.Controller()
        self.espeak = ESpeakNG()
        
        self.head = HeadController(self.master_controller) # Removed 3 and 1000. I don't know why these are here
        self.wheels = WheelController(self.master_controller)
        self.waist = WaistController(self.master_controller)
        self.voice = Voice(self.espeak)
        self.arm = ArmController(self.master_controller)
        self.robot_controller = RobotController(self)
        self.speech_engine = AlDialogEngine(path=speech_engine_path)
        pass
    def close(self):
        self.master_controller.close()

    def StopAllChannels(self):
        for channel in self.__MOTORCHANNELS:
            if(self.master_controller.isMoving(channel)): 
                self.master_controller.setSpeed(channel,self.master_controller.getPosition(channel))
        self.turn_wheels(6000)
        self.drive_wheels(6000)

    def ResetServoPositions(self):
        for channel in self.__MOTORCHANNELS:
            if(channel != 0 and channel != 1):
                self.master_controller.setTarget(channel, 6000)

    def pan_head(self, angle):
        self.head.pan(angle, 3)

    def tilt_head(self, angle):
        self.head.tilt(angle, 4)

    def rotate_waist(self, angle):
        self.waist.rotate(angle, 5)

    def speak(self, message):
        self.voice.say(message)

    def drive_wheels(self, speed):
        self.wheels.drive(speed, 0)

    def turn_wheels(self, speed):
        self.wheels.drive(speed, 1)

    def raise_arm(self, angle):
        self.arm.Raise(angle, 6)

    def is_front_blocked(self):
        return self.robot_controller.IsFrontBlocked()

    def is_rear_blocked(self):
        return self.robot_controller.IsRearBlocked()

    def add_action_via_str(self, action_value):
        self.robot_controller.AddActionViaStr(action_value)

    def update_action_state(self):
        self.robot_controller.Update()

    def reset_state(self):
        self.robot_controller.Reset()

    def queue_actions(self, actions):
        for action in actions:
            action_value: str = action.get_value()
            self.add_action_via_str(action_value)
            self.update_action_state()

    def reset_robot_dialog_and_state(self):
        self.reset_state()
        self.speech_engine.reset_dialog()

    def get_response(self, question_words) -> tuple[list, str]:
        return self.speech_engine.get_response(question_words)
