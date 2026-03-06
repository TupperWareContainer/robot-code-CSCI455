from maestro import Controller



class ArmController:
    __controller : Controller

    def __init__(self, controller : Controller):
        self.__controller = controller

    

    def Raise(self,angle, chan):
        self.__controller.setRange(chan, 0, 0)
        self.__controller.setSpeed(chan, 0)
        self.__controller.setAccel(chan, 0)
        self.__controller.setTarget(chan, angle)
