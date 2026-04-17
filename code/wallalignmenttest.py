from robot import Robot
from robot_controller import RobotController

robot = Robot()
controller = RobotController(robot, 270, 90)
controller.turn(6000)


try:

    while (True):
        controller.AlignWithLeftWall()
except KeyboardInterrupt:
    pass
finally:
    controller.turn(6000)

