from adafruit_rplidar import RPLidar
from threading import Thread



class LidarController:
    __lidar : RPLidar
    __max_distance : float
    __scan_data = [0] * 360
    __scan_thread : Thread
    __stopScan : bool
    def __init__(self, lidar_port : str, timeout : float, max_distance : float):
        self.__lidar = RPLidar(None, lidar_port, timeout)
        self.__max_distance = max_distance
        self.__stopScan = False
        self.__scan_thread = Thread(target = self.StartScan())
        self.__scan_thread.start()

    def StartScan(self):
        for scan in self.__lidar.iter_scans():
            for _, angle, distance in scan:
                self.__scan_data[min([359,floor(angle)])] = distance
            if self.__stopScan:
                return;
    def StopScan(self):
        self.__stopScan = True
        self.__scan_thread.join()

    def GetDistanceInches(self, angle : int):
        if(angle < 360):
            return self.__scan_data[angle] * 0.03937
        else:
            return -1


        

    
            
