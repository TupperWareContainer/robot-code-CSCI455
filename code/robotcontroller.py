from robot import Robot
from enum import Enum
'''
RobotController.py
Command Based Interface for controlling a Robot instance

'''



class RobotAction(Enum):
    NONE = 0 
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
    __scope : list[str]
    __actionQueue : list[RobotAction]
    __state : RobotState
    def __init__(self):
        self.__actionQueue = list[RobotAction]
        self.__state = RobotState.BOOT
        self.__robotInstance = Robot()
        self.__scope = list[str]

   
    def __StateMachine(self):
        match self.__state:
            case RobotState.BOOT:
                pass
            case RobotState.ACTION_EXEC:
                pass
            case _:
                pass



    def AddAction(self, action : RobotAction):
        self.__actionQueue.append(action) 

    

    def GetState(self) -> RobotState:
        pass

    def GetCurrentAction(self) -> RobotAction: 
        if (len(self.__actionQueue) <= 0):
            return RobotAction.NONE
        else: 
            return self.__actionQueue[0]


    
    def GetScope(self) -> list[str]:
        return self.__scope
