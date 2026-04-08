"""
channel_config.py

powers each channel individually to find which channel belongs to which subsystem
"""
import time

from robot import Robot

channel_map : list[(str,str)] = list()


def print_map():
    for mapping in channel_map:
        print(str(mapping))




print("Initializing Robot\n")
bot = Robot()


speed = 25
next_channel = False
for i in range(24):
    next_channel = False 
    while (not next_channel):
        print("mappings:")
        print_map()
        print("running channel " + str(i) + "\n")
        bot.drive_wheels(speed, i)
        time.sleep(1)
        bot.drive_wheels(0, i)

        print("did this move anything? [y/n]\n")

        answer = (str(input()).strip()).lower()


        if answer == "y": 
            print("what subsystem moved? (left_wheel, right_wheel, head, waist, etc)\n")

            subsystem = input()
            
            mapping = (subsystem, str(i))

            print("adding mapping to list: " + str(mapping) + "\n")
            channel_map.append(mapping) 
            next_channel = True
        elif answer == "n":
            print("Moving to next subsystem...\n");
            next_channel = True

        



print("Mapping finished... writing mapping to mapping.csv\n")



with open("mapping.csv", "w") as f:
    to_write : str = ""
    for mapping in channel_map:
        to_write += mapping[0] + "," + mapping[1]
    f.write(to_write) 

bot.close()
