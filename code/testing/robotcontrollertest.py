from robotcontroller import RobotController, RobotAction, RobotState





cont = RobotController()


print("Initialized Robot Controller")

inp = input()

cont.AddAction(RobotAction.HEAD_YES)
print("Added action HEAD_YES")

inp = input()

cont.AddAction(RobotAction.HEAD_NO)
print("Added action HEAD_NO")

inp = input()

cont.Update()
print("Updating...")

inp = input()


cont.Update()
print("Updating...")
inp = input()

cont.AddAction(RobotAction.NONE)
print("Added action NONE")

inp = input()

cont.Update()
print("Updating")

inp = input()
