from maestro import Controller
# Wheel Channels = 14 & 15

class WheelController:
    controller : Controller 

    __MOTOR_MIN = 1200 
    __MOTOR_MAX = 1800
    def __init__(self, controller : Controller):
        self.controller = controller
        pass

    def drive(self, speed, chan):
        # 1200 min 1800 max
        self.controller.setSpeed(0, 23)
        self.controller.setSpeed(1, 23)

        self.controller.setRange(chan, 0, 0)
        self.controller.setTarget(chan, speed)


	
