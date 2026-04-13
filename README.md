# README.md

# PROJECT 4

## Notes

Let X be the angle we want to be aligned with with the wall. 
Let S1, S2 be sets of angle pairs that are equadistant from X (e.g. X = 180, S1 = {180 - 5, 180 - 10, 180 - 15}, S2 = {180 + 5, 180 + 10, 180 + 15)


We can consider the robot to be "aligned" with the wall if the following statement evaluates as true.
forall a in S1, forall b in S2 | distanceAt(a) = distanceAt(b). 


As for actually following the wall, it could be abstracted into robot_controller.

```python 
def AlignWithWall():    # aligns the robot with the wall 
```


# PROJECT 3
## Robot Safety Limits
- Front blocked if any reading from 330-360 degrees or 0-30 degrees is under 800 mm
- Rear blocked if any reading from 150-210 degrees is under 800 mm

## TODO:
    1. make robot safety aware using lidar (object detection)
        - Forward Saftey Stop 
        - Backward Safety Stop

# PROJECT 2

## TODO: 
1. Dialog parser
2. Robot State Machine
    - Robot Actions





# PROJECT 1
## The data Received from the controller
- The joystick x and y positions
- The angles for the waist, head tilt, and head pan
- The messages "Hello Hunter", “Hunter is so cool.”, “Please don't touch my wheels.”, and “Hunter is the greatest.”

### Wheels 
8000 = reverse, 6000 = stop, 4000 = forward
### Head Servos
8000 = up/left, 6000 = mid, 4000 = down/right
### Waist Servos
8000 = right, 6000 = mid, 4000 = right
