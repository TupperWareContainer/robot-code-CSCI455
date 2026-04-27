from robot_controller import RobotController


def StartFinalProjectBehavior(controllerInstance : RobotController):
    while(not controllerInstance.IsFrontBlocked()):
        continue

    controllerInstance.SpeakPhrase("Hello, How Can I Help?") 
    # poll audio until special phrase is spoken

      
    
    # set destination depending on phrase
    pass





def PathToBathroom(controllerInstance : RobotController):
      

    pass

def PathToLab(controllerInstance : RobotController):
    pass
