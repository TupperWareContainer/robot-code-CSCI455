import os
from math import floor
from rplidar import RPLidar

LIDAR_PORT = '/dev/ttyUSB0'

lidar = RPLidar(LIDAR_PORT, timeout = 3)

max_distance = 0


def process_data(data):
    if len(data) == 0: 
        return
    os.system('cls' if os.name == 'nt' else 'clear')

    
    for i in range (0,359, 20):
        print(str(i) + ": " + str(data[i]) + "\n")


scan_data = [0]*360

try:
    for scan in lidar.iter_scans():
        for(_, angle, distance) in scan:
            scan_data[min([359,floor(angle)])] = distance
            
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping")

lidar.stop()
lidar.disconnect()
