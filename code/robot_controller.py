import threading
import time
from robot_actions import PerformHeadNod, ShakeHead, RaiseArm, Dance90
from lidar_controller import LidarController
from enum import Enum
from collections import deque
import os
'''
RobotController.py
Command Based Interface for controlling a Robot instance

'''

LIDAR_PORT = '/dev/ttyUSB0'
STOP_DISTANCE = 1000
BODY_SIZE = 250

# the number of alignemnt measurements to take per side (eg 10 measurements per side means 20 total measurements)
NUM_ALIGNMENT_MEASUREMENTS_PER_SIDE = 25
ALIGNMENT_OK_PERCENT = 0.75


ALIGNMENT_ANGLE_INCREMENT = 1

MIN_ALIGNMENT_MEASUREMENTS = 4



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
    WALL_FOLLOW = 5

class RobotController:
    __scope : list[str]
    __actionQueue : deque[RobotAction]
    __state : RobotState

    __isPerformingAction : bool
    __isSafetyTimerActive : bool

    __cSafetyTime : float
    
    __wallLeftAngle : int

    __wallRightAngle : int

    __safety_thread : threading.Thread

    def __init__(self, robot_instance, wall_left_angle, wall_right_angle):
        self.__actionQueue = deque[RobotAction]()
        self.__state = RobotState.BOOT
        self.__robotInstance = robot_instance
        self.__scope = list[str]
        self.__isPerformingAction = False
        self.__isSafetyTimerActive = False
        self.__lastSafetyTime = -1
        self.__maxSafetyTime = 0
        self.__safeTimeSet = False
        self._is_front_blocked = False
        self._is_rear_blocked = False
        self.__wallLeftAngle = wall_left_angle
        self.__wallRightAngle = wall_right_angle
        
        self._lidar_controller = LidarController(LIDAR_PORT, timeout=3, max_distance=0)

        self.__safety_thread = threading.Thread(target=self.__SafetyTimer)
        self.__safety_thread.start()
    
    def AlignWithLeftWall(self) -> bool: 
        print("ALIGNING WITH LEFT WALL")
        alignment_data  = [] # distance, distance, angle A, angle B, delta angle (from left angle), delta distance

        for i in range(0, NUM_ALIGNMENT_MEASUREMENTS_PER_SIDE):
            angle = (i + 1) * ALIGNMENT_ANGLE_INCREMENT
            a = self.__wallLeftAngle + angle
            b = self.__wallLeftAngle - angle
            
            if(a > 360):
                a = a - 360 
            if(b < 0 ):
                b = 360 + b

            dA = self._lidar_controller.GetDistanceMM(a)
            dB = self._lidar_controller.GetDistanceMM(b)
            
            if (dA == 0.0 or dB == 0.0) :
                continue
            delta_distance = abs(dA) - abs(dB) ## positive delta = needs to rotate CCW, negative delta = needs to rotate CW 
            result = (dA, dB, a,b,angle, delta_distance)
            alignment_data.append(result)
            
        if(len(alignment_data) / MIN_ALIGNMENT_MEASUREMENTS < ALIGNMENT_OK_PERCENT):
            print("RobotController::AlignWithLeftWall() Failed : Insufficient number of alignment measurements!")
            return False
        deltas  = [] # delta angle, delta distance
        
        total = 0.0
        for data in alignment_data:
            total += data[5]
        num_data_points = len(alignment_data)
        avg = total * 1.0 / (1 if (num_data_points == 0) else num_data_points)
       
        if(abs(avg) < 10):
            avg = 0
        
        print(str(avg))
        if(avg > 0):    # turn CCW
            self.turn(8000)
            print("turning CCW,")
            pass
        elif(avg < 0): # turn CW
            self.turn(4000)
            print("turning CW")
            pass
        else:           # aligned
            self.turn(6000)
            print("aligned")
            pass
        
        print("RobotController::AlignWithLeftWall() Succeeded")

        return False

    def AlignWithRightWall(self) -> bool:
          
        pass

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

    def __IsBlocked(self, angles: list[int]) -> bool:
        distances = []
        for a in angles:
            distances.append(self._lidar_controller.GetDistanceMM(a))

        readings = [(angle, distance) for angle in angles for distance in distances]
        non_zero = [distance for (a,distance) in readings if distance != 0]
                
        # If all readings are 0, no lidar data — fail safe and block
        if len(non_zero) == 0:
            print("Not initialized")
            return True

        # Filter out robot's own body readings
        external = [(angle,distance) for (angle,distance) in readings if distance > BODY_SIZE]

        # If nothing external detected, path is clear
        if len(external) == 0:
            return False
        return any(d < STOP_DISTANCE for (a,d) in external)

    def IsFrontBlocked(self) -> bool:
        front_angles = list(range(350, 360)) + list(range(0, 10))  # Front angles: 350-359 and 0-9
        is_front_blocked = self.__IsBlocked(front_angles)

        if is_front_blocked:
            print("Front is BLOCKED")

        return is_front_blocked

    def IsRearBlocked(self) -> bool:
        rear_angles = list(range(170, 190)) # Rear angles: 170 to 189
        is_rear_blocked = self.__IsBlocked(rear_angles)

        if is_rear_blocked:
            print("Rear is BLOCKED")

        return is_rear_blocked

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

    def stop_drive(self):
        self.__robotInstance.turn_wheels(6000)
        self.__robotInstance.drive_wheels(6000)

    def WallFollowTick(self):
        try:
            while True:
                self.__wallfollowstate = "ALIGN_LEFT"
                ## update resulting state and then plug into this function


                self.WallFollowStateMachine(self.__wallfollowstate)
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_drive()
            self.AlignWithLeftWall()
            print("Stopping...")
    def WallFollowStateMachine(self, wallFollowState):
        if(wallFollowState == "ALIGN_LEFT"):
            self.AlignWithLeftWall()
        elif(wallFollowState == "ALIGN_RIGHT"):
            self.AlignWithRightWall()
        else: # check if front or back is blocked and drive from there
            return
    def pan_head(self, rot : int):
        self.__robotInstance.pan_head(rot)

    def tilt_head(self, rot : int):
        self.__robotInstance.tilt_head(rot)

    def rotate_waist(self, rot : int):
        self.__robotInstance.rotate_waist(rot)

    def drive(self, speed):
        self.__robotInstance.drive_wheels(speed)

    def turn(self, speed):
        self.__robotInstance.turn_wheels(speed)

    def queue_actions(self, actions):
        for action in actions:
            action_value: str = action.get_value()
            self.AddActionViaStr(action_value)
            self.Update()

    def reset_robot_dialog_and_state(self):
        self.Reset()
        self.__robotInstance.reset_dialog()

    def get_dialog_response(self, question_words) -> tuple[list, str]:
        return self.__robotInstance.get_response(question_words)

    def close_robot(self):
        self.__robotInstance.close()

    def speak_message(self, message : str):
        self.__robotInstance.speak(message)
