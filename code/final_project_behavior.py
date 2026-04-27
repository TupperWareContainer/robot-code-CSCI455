from robot_controller import RobotController
import time

def StartFinalProjectBehavior(controllerInstance : RobotController):
    while(not controllerInstance.IsFrontBlocked()):
        continue

    controllerInstance.SpeakPhrase("Hello, How Can I Help?") 
    # poll audio until special phrase is spoken

      
    
    # set destination depending on phrase
    pass

def FinalProjectInitialization(controllerInstance: RobotController):
    
    ## turn 180 degrees
    controllerInstance.steer_right()
    time.sleep(1.4)
    controllerInstance.stop_steer()
   
    # TODO: find a way to modify this value
    destination = "Lab"
    
    startnextstage = False

    while(startnextstage == False):
        controllerInstance.drive(4500)
        if(controllerInstance.IsFrontBlocked()):
            controllerInstance.stop_drive()
            time.sleep(4)
            startnextstage = controllerInstance.IsFrontBlocked()
            continue  
    
    controllerInstance.stop_drive()
     
    if(destination == "Lab"):
        PathToLab(controllerInstance)
    elif (destination == "Bathroom"):
        PathToBathroom(controllerInstance)
    
    pass


def PathToBathroom(controllerInstance : RobotController):
       

    pass

def PathToLab(controllerInstance : RobotController):
    pass
