import threading
import time
from robot_actions import PerformHeadNod, ShakeHead, RaiseArm, Dance90
from lidar_controller import LidarController
from enum import Enum
from collections import deque
'''
RobotController.py
Command Based Interface for controlling a Robot instance

'''

LIDAR_PORT = '/dev/ttyUSB0'
STOP_DISTANCE = 900
BACK_BODY_SIZE = 20
FRONT_BODY_SIZE = 20

class RobotAction(Enum):
    UNKNOWN = -1
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
    __scope : list[str]
    __actionQueue : deque[RobotAction]
    __state : RobotState

    __isPerformingAction : bool
    __isSafetyTimerActive : bool

    __cSafetyTime : float

    __safety_thread : threading.Thread

    def __init__(self, robot_instance):
        self.__actionQueue = deque[RobotAction]()
        self.__state = RobotState.BOOT
        self.__robotInstance = robot_instance
        self.__scope = list[str]
        self.__isPerformingAction = False
        self.__isSafetyTimerActive = False
        self.__lastSafetyTime = -1
        self.__maxSafetyTime = 0
        self.__safeTimeSet = False

        self._lidar_controller = LidarController(LIDAR_PORT, timeout=3, max_distance=0)

        self.__safety_thread = threading.Thread(target=self.__SafetyTimer)

        self.__safety_thread.start()

    def Update(self):
        if (len(self.__actionQueue) > 0) or self.__isPerformingAction: 
            self.__state = RobotState.ACTION_EXEC
        else: 
            self.__state = RobotState.IDLE

        
        self.__StateMachine()

    
    def __SafetyTimer(self):
        if(self.__isSafetyTimerActive):
            print("WARNING : ATTEMPTED CALL OF SAFETY TIMER WHILE TIMER IS ALREADY ACTIVE! Refusing to call method...")
            return
        self.__isSafetyTimerActive = True
        while(True):
            if(not self.__safeTimeSet or not self.__isPerformingAction):
                continue
            elif(time.time() - self.__lastSafetyTime >= self.__maxSafetyTime):
                self.__robotInstance.StopAllChannels()
                self.__robotInstance.ResetServoPositions()

                self.__safeTimeSet = False
            time.sleep(1)

    def IsFrontBlocked(self) -> bool:
        front_angles = list(range(330, 360)) + list(range(0, 31))  # 330-359 and 0-30
        is_front_blocked = any(
            distance < STOP_DISTANCE
            for angle in front_angles
            if (distance := self._lidar_controller.GetDistanceMM(angle)) != 0
        )

        for angle in front_angles:
            print("Distance", self._lidar_controller.GetDistanceMM(angle))

        if is_front_blocked:
            print("Front is BLOCKED")

        return is_front_blocked

    def IsRearBlocked(self) -> bool:
        rear_angles = list(range(175, 185)) # 150 to 210
        is_rear_blocked = any(
            distance < STOP_DISTANCE
            for angle in rear_angles
            if (distance := self._lidar_controller.GetDistanceMM(angle)) != 0
        )
        
        if is_rear_blocked:
            print("Rear is BLOCKED")

        return is_rear_blocked

    def CanMove(self, direction: str) -> bool:
        try:
            if direction == "forward":
                return not self.IsFrontBlocked()
            elif direction == "backward":
                return not self.IsRearBlocked()
            return False
        except Exception as e:
            print(f"Error checking movement: {e}")
        return False

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
                self.__maxSafetyTime = 3

                self.__lastSafetyTime = time.time()
                self.__safeTimeSet = True
                PerformHeadNod(self.__robotInstance)
                pass
            case RobotAction.HEAD_NO:
                self.__maxSafetyTime = 3

                self.__lastSafetyTime = time.time()
                self.__safeTimeSet = True

                ShakeHead(self.__robotInstance)
                pass
            case RobotAction.ARM_RAISE:
                self.__maxSafetyTime = 4

                self.__lastSafetyTime = time.time()
                self.__safeTimeSet = True
                RaiseArm(self.__robotInstance)
                pass
            case RobotAction.DANCE_90:
                self.__maxSafetyTime = 6

                self.__lastSafetyTime = time.time()
                self.__safeTimeSet = True
                Dance90(self.__robotInstance)
                pass

            case RobotAction.NONE:
                pass
            case RobotAction.UNKNOWN:
                print("WARNING: UNKNOWN ACTION EXECUTION ATTEMPT DETECTED, DOING NOTHING...")
                pass
            case _:
                pass 

        self.__isPerformingAction = False


    def AddAction(self, action : RobotAction):
        self.__actionQueue.append(action)

    def AddActionViaStr(self, action : str):
        temp = action.lower()
        print("Adding action \"" + temp + "\"")
        match temp:
            case "head_yes":
                self.AddAction(RobotAction.HEAD_YES)
                pass
            case "head_no":
                self.AddAction(RobotAction.HEAD_NO)
                pass
            case "arm_raise":
                self.AddAction(RobotAction.ARM_RAISE)
                pass
            case "dance90":
                self.AddAction(RobotAction.DANCE_90)
                pass
            case _:
                print("Warning: Unknown action: \"" + temp + "\", adding action of type UNKNOWN to action queue...")
                self.AddAction(RobotAction.UNKNOWN)
                pass
        
    def SpeakPhrase(self, phrase : str):
        self.__robotInstance.speak(phrase)


    def GetState(self) -> RobotState:
        return self.__state

    def GetCurrentAction(self) -> RobotAction: 
        if (len(self.__actionQueue) <= 0):
            return RobotAction.NONE
        else: 
            return self.__actionQueue[0]

    
    def Reset(self):
        self.__actionQueue.clear()
        self.__isPerformingAction = False
        self.__isSafetyTimerActive = False
        self.__state = RobotState.IDLE
        self.__robotInstance.StopAllChannels()
        self.__robotInstance.ResetServoPositions()

    def GetScope(self) -> list[str]:
        return self.__scope
