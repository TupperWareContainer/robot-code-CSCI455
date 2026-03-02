from robot import Robot

r = Robot()
speed = 8000

r.tilt_head(6000)
i = input()


r.tilt_head(speed)
print("Speed = " + str(i))

i = input()

r.tilt_head(6000)
r.close()




