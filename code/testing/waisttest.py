# motor channels = 14 & 15

from robot import Robot
import time

r = Robot()
speed = 0



i = "y"

while((i == "n") == False):

    print("please enter a speed (n to quit):")
    i = input()
    speed = int(i)

    r.rotate_waist(speed)


r.rotate_waist(6000)
r.close()

