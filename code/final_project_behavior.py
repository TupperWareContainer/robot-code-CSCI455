from threading import Thread, Event

from robot_controller import RobotController
import time
from enum import Enum

class RobotState(Enum):
    WAITING             = 0
    GREETING            = 1
    LISTENING           = 2
    TURNING_AROUND      = 3
    ALIGNING_TO_HALLWAY = 4
    MOVING_TO_T         = 5
    TURNING_TO_DESTINATION = 6
    FINAL_MOVEMENT      = 7
    STOPPED             = 8

current_state = RobotState.WAITING

def set_state(new_state: RobotState):
    global current_state
    current_state = new_state

def StartFinalProjectBehavior(controllerInstance : RobotController):
    time.sleep(4)

    set_state(RobotState.WAITING)
    while(not controllerInstance.IsFrontBlocked()):
        time.sleep(0.1) # This is so we don't starve other threads.
        continue

    set_state(RobotState.GREETING)
    controllerInstance.SpeakPhrase("Hello, How Can I Help?")

    # Change to the listening state and wait till the robot is done speaking.
    set_state(RobotState.LISTENING)
    while not controllerInstance.get_destination():
        time.sleep(0.1)
        continue
    FinalProjectInitialization(controllerInstance)

    destination = controllerInstance.get_destination()
    controllerInstance.SpeakPhrase(destination + " follow me")

    set_state(RobotState.FINAL_MOVEMENT)
    pass

# Called in the greet flask route to initialize the pathing
def FinalProjectInitialization(controllerInstance: RobotController):
    
    ## turn 180 degrees
    set_state(RobotState.TURNING_AROUND)
    controllerInstance.steer_right()
    time.sleep(1.4)
    controllerInstance.stop_steer()
    
    startnextstage = False

    while(startnextstage == False):
        controllerInstance.drive(4500)
        if(controllerInstance.IsFrontBlocked()):
            controllerInstance.stop_drive()
            time.sleep(4)
            startnextstage = controllerInstance.IsFrontBlocked()
            continue

    set_state(RobotState.MOVING_TO_T)
    controllerInstance.stop_drive()
    destination = controllerInstance.get_destination()
     
    if(destination == "Lab"):
        PathToLab(controllerInstance)
    elif (destination == "Bathroom"):
        PathToBathroom(controllerInstance)
    else:
        controllerInstance.SpeakPhrase("Sorry, I don't know that destination.")
        set_state(RobotState.STOPPED)


def PathToBathroom(controllerInstance : RobotController):
    controllerInstance.SetWallDesired("right")
    controllerInstance.WallFollowTick()

def PathToLab(controllerInstance : RobotController):
    controllerInstance.SetWallDesired("left")
    controllerInstance.WallFollowTick()
