from head_controller import HeadController
from waist_controller import WaistController
from wheel_controller import WheelController
from arm_controller import ArmController
from voice import Voice
from espeakng import ESpeakNG
import maestro
class Robot:
    master_controller : maestro.Controller
    espeak  : ESpeakNG
    head    : HeadController
    wheels  : WheelController
    waist   : WaistController
    arm     : ArmController
    voice   : Voice

    def __init__(self):
        # Add the logic for tty1 vs tty0 here
        self.master_controller = maestro.Controller()
        self.espeak = ESpeakNG()

        self.head = HeadController(self.master_controller)
        self.wheels = WheelController(self.master_controller)
        self.waist = WaistController(self.master_controller)
        self.voice = Voice(self.espeak)
        pass
    def close(self):
        self.master_controller.close()


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
