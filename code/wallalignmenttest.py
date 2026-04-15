from robot import Robot
from robot_controller import RobotController

robot = Robot()
controller = RobotController(robot, 90, 270)

inp = input("Press enter to continue")

while (True):
    controller.AlignWithLeftWall()



