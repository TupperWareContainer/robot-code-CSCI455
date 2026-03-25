import os
from math import floor
from adafruit_rplidar import RPLidar

LIDAR_PORT = '/dev/ttyUSB0'

lidar = RPLidar(None, LIDAR_PORT, timeout = 3)




max_distance = 0


def process_data(data):
    if len(data) == 0: 
        return
    os.system('cls' if os.name == 'nt' else 'clear')

    

    print("0: " + str(data[0]) + "\n");
    print("45:" + str(data[45]) + "\n"); 
    print("90:" + str(data[90]) + "\n");
    print("135:" + str(data[135]) +"\n");
    print("180" + str(data[180]) + "\n");

scan_data =  [0]*360

try:
    for scan in lidar.iter_scans():
        for(_, angle, distance) in scan:
            scan_data[min([359,floor(angle)])] =distance
            
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping")

lidar.stop()
lidar.disconnect()
