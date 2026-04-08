from robot import Robot

r = Robot()
speed = 8000

print("Head Tilt")

r.tilt_head(6000)
i = input()


r.tilt_head(speed)
print("Speed = " + str(speed))


i = input()

r.tilt_head(6000)

i = input()
speed = 4000


r.tilt_head(speed)
print("Speed = " + str(speed))


i = input()

r.tilt_head(6000)

print("Head Pan")

speed = 8000

r.pan_head(6000)
i = input()


r.pan_head(speed)
print("Speed = " + str(speed))

i = input()

r.pan_head(6000)

i = input()
speed = 4000

r.pan_head(speed)
print("Speed = " + str(speed))

i = input()

r.pan_head(6000)

print("Waist")

r.rotate_waist(6000)

i = input()
speed = 8000
print("Speed = " + str(speed))
r.rotate_waist(speed)

i = input()

speed = 4000

print("Speed = " + str(speed))
r.rotate_waist(speed)

i = input()

r.rotate_waist(6000)

r.close()




