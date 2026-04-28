from robot_controller import RobotController
from final_project_behavior import *
from robot import Robot
r = Robot("./testDialogFileForPractice.txt")
cont = RobotController(r,270,90 )




print("Initialization")
FinalProjectInitialization(cont)


print("Done")
exit()
