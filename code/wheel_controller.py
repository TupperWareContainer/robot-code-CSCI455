from maestro import Controller
# Wheel Channels = 14 & 15

class WheelController:
    controller : Controller 

    __MOTOR_MIN = 1200 
    __MOTOR_MAX = 1800
    NEUTRAL = 6000
    def __init__(self, controller : Controller):
        self.controller = controller
        pass

    def drive(self, speed, chan):
        # 1200 min 1800 max
        # Scale the offset from neutral to 75%
        if speed != WheelController.NEUTRAL:
            offset = speed - WheelController.NEUTRAL

            limited = WheelController.NEUTRAL + int(offset * 0.6)
            limited = max(4000, min(8000, limited))
        else:
            limited = WheelController.NEUTRAL # If we are trying to stop we don't need to limit it.

        print("driving " + str(limited) + " to channel " + str(chan) )
        self.controller.setRange(chan, 0, 0)
        self.controller.setTarget(chan, limited)


	
