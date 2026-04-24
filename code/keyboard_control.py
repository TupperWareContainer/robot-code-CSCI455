from robot import Robot
from sshkeyboard import listen_keyboard
import time

r = Robot()

r.drive_wheels(6000)

def press(key):
    match key:
        case 'w':
            r.drive_wheels(4000)
        case 'a': 
            r.turn_wheels(8000)
        case 's': 
            r.drive_wheels(8000)
        case 'd': 
            r.turn_wheels(4000)
        case 'q':
            r.drive_wheels(6000)
            r.turn_wheels(6000)
        case _:
            return
def release(key):
    r.drive_wheels(6000)
    r.turn_wheels(6000)


listen_keyboard(on_press=press,sequential=True,on_release=release)
print("closing")
r.close()
