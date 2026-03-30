from adafruit_rplidar import RPLidar
from math import floor
from threading import Thread



class LidarController:
    __lidar : RPLidar
    __max_distance : float
    __scan_thread : Thread
    __stopScan : bool
    def __init__(self, lidar_port : str, timeout : float, max_distance : float):
        self.__scan_data = [0.0] * 360
        self.__lidar = RPLidar(None, lidar_port, timeout)
        self.__max_distance = max_distance
        self.__stopScan = False
        self.__scan_thread = Thread(target = self.StartScan)
        self.__scan_thread.start()

    def StartScan(self):
        try:
            for scan in self.__lidar.iter_scans(max_buf_meas=1000):
                for _, angle, distance in scan:
                    idx = min([359, floor(angle)])
                    self.__scan_data[idx] = distance
                if self.__stopScan:
                    self.__lidar.stop()
                    return;
        except Exception as e:
            print(f"Lidar Error: {e}")
            self.__lidar.clear_input()

    def StopScan(self):
        self.__stopScan = True
        self.__scan_thread.join()

    def GetDistanceInches(self, angle : int):
        if(angle < 360):
            return self.__scan_data[angle] * 0.03937
        else:
            return -1

    def GetDistanceMM(self, angle : int):
        clean_angle = int(angle % 360)

        return self.__scan_data[clean_angle]
        

    
            
