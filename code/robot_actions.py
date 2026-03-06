import time
from robot import Robot

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