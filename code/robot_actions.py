import time
from robot import Robot

## TODO: Dance90

def PerformHeadNod(robotInstance : Robot):
    print("Nodding Head")
    robotInstance.tilt_head(8000)
    time.sleep(1.5)
    robotInstance.tilt_head(4000)
    time.sleep(1.5)
    robotInstance.tilt_head(6000)
    time.sleep(1.5)
    return

def ShakeHead(robotInstance : Robot):
    print("Shaking Head")
    robotInstance.pan_head(4000)
    time.sleep(1.5)
    robotInstance.pan_head(8000)
    time.sleep(1.5)
    robotInstance.pan_head(6000)
    time.sleep(1.5)
    return

def RaiseArm(robotInstance : Robot):
    print("Raising Arm")
    robotInstance.raise_arm(8000)
    time.sleep(1.5)
    robotInstance.raise_arm(6000)



def Dance90(robotInstance : Robot):
    print("Dancing 90")
    robotInstance.drive_wheels(6000)
    time.sleep(0.125)
    robotInstance.turn_wheels(7000)
    time.sleep(1.5)
    robotInstance.turn_wheels(6000)
    time.sleep(1.5)
    robotInstance.turn_wheels(5000)
    time.sleep(1.0)
    robotInstance.turn_wheels(6000)
