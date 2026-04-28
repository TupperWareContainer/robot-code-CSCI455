from threading import Thread, Event

from robot_controller import RobotController
import time

greeting_done = Event()

def StartFinalProjectBehavior(controllerInstance : RobotController):
    while(not controllerInstance.IsFrontBlocked()):
        time.sleep(0.1) # This is so we don't starve other threads.
        continue

    controllerInstance.SpeakPhrase("Hello, How Can I Help?")
    greeting_done.set()

    wall_follow_thread = Thread(target=controllerInstance.WallFollowTick)
    wall_follow_thread.start()
    pass

# Called in the greet flask route to initialize the pathing
def FinalProjectInitialization(controllerInstance: RobotController):
    
    ## turn 180 degrees
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
    
    controllerInstance.stop_drive()
    destination = controllerInstance.get_destination()
     
    if(destination == "Lab"):
        PathToLab(controllerInstance)
    elif (destination == "Bathroom"):
        PathToBathroom(controllerInstance)
    else:
        controllerInstance.SpeakPhrase("Sorry, I don't know that destination.")


def PathToBathroom(controllerInstance : RobotController):
    controllerInstance.SetWallDesired("right")

def PathToLab(controllerInstance : RobotController):
    controllerInstance.SetWallDesired("left")
