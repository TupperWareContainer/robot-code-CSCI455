from robot import Robot
from enum import Enum

class RobotAction(Enum):
    HEAD_YES = 1
    HEAD_NO = 2
    ARM_RAISE = 3
    DANCE_90 = 4

class RobotState(Enum):
    BOOT = 1
    IDLE = 2
    IN_SCOPE = 3
    ACTION_EXEC = 4

class RobotController:
    __robotInstance : Robot
    def __init__(self):
        self.__robotInstance = Robot()
        self.__rule_scope = (-1,-1)


    def DoAction(action : RobotAction):
        pass

    def GetState() -> RobotState:
        pass

    def GetCurrentAction() -> RobotAction:
        pass

