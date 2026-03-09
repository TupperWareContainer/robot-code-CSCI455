import robot_actions
from robot import Robot
from enum import Enum
from collections import deque 
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
    __actionQueue : deque[RobotAction]
    __state : RobotState

    __isPerformingAction : bool

    def __init__(self):
        self.__actionQueue = deque[RobotAction]()
        self.__state = RobotState.BOOT
        self.__robotInstance = Robot()
        self.__scope = list[str]
        self.__isPerformingAction = False

    def Update(self):
        if (len(self.__actionQueue) > 0) or self.__isPerformingAction: 
            self.__state = RobotState.ACTION_EXEC
        else: 
            self.__state = RobotState.IDLE

        
        self.__StateMachine()

    
    def __StateMachine(self):
        match self.__state:
            case RobotState.BOOT:
                pass
            case RobotState.ACTION_EXEC:
                self.__PerformAction()
                pass
            case _:
                pass

    def __PerformAction(self):
        actionID : RobotAction = self.__actionQueue.pop()

        match actionID:
            case RobotAction.HEAD_YES:
                robot_actions.PerformHeadNod(self.__robotInstance)
                pass
            case RobotAction.HEAD_NO:
                robot_actions.ShakeHead(self.__robotInstance)
                pass
            case RobotAction.ARM_RAISE:
                robot_actions.RaiseArm(self.__robotInstance)
                pass
            case RobotAction.DANCE_90:
                robot_actions.Dance90(self.__robotInstance)
                pass

            case RobotAction.NONE:
                pass
            case _:
                pass 


    def AddAction(self, action : RobotAction):
        self.__actionQueue.append(action)

    def AddActionViaStr(self, action : str):
        pass
    

    def GetState(self) -> RobotState:
        pass

    def GetCurrentAction(self) -> RobotAction: 
        if (len(self.__actionQueue) <= 0):
            return RobotAction.NONE
        else: 
            return self.__actionQueue[0]


    
    def GetScope(self) -> list[str]:
        return self.__scope
