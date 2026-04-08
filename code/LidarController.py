from rplidar import RPLidar, RPLidarException
from math import floor
from threading import Thread
import time

class LidarController:
    __lidar : RPLidar
    __max_distance : float
    __scan_thread : Thread
    __stopScan : bool
    __lidar_port : str 
    __timeout : float
    __scan_data = [0.0] * 360

    def __init__(self, lidar_port : str, timeout : float, max_distance : float):
        self.__lidar = RPLidar(lidar_port, timeout=timeout)
        self.__lidar_port = lidar_port
        self.__timeout = timeout 
        self.__max_distance = max_distance
        self.__stopScan = False
        self.__scan_thread = Thread(target = self.StartScan)
        self.__scan_thread.start()

    def StartScan(self):
        try:
            print("Cleaning up Lidar state")
            self.__lidar.stop() 
            self.__lidar.disconnect()
            self.__lidar.connect()
        except Exception as e:
            print(f"Unexpected Error: {e}")
        try:
            while not self.__stopScan:
                 # print("Scanning")
                 # iter_scans is a blocking generator
                for scan in self.__lidar.iter_scans():
                    for (_, angle, distance) in scan:
                        idx = min([359, floor(angle)])
                        LidarController.__scan_data[idx] = distance

                    time.sleep(0.1)  # Yields control to other threads
        except RPLidarException as e:
                # This is where 'line length mismatch' is caught
            print(f"Lidar Hardware Error: {e}. Reconnecting...")
            self.RebootLidar() 
        except Exception as e:
            self.RebootLidar()
        finally:
            self.StartScan()
    def RebootLidar(self):
        self.__lidar.stop()
        self.__lidar.disconnect()
       
        self.__lidar = RPLidar(self.__lidar_port, timeout=self.__timeout)
        
    def StopScan(self):
        self.__stopScan = True
        self.__scan_thread.join()

    def GetDistanceMM(self, angle : int):
        clean_angle = int(angle % 360)
        distance_mm = LidarController.__scan_data[clean_angle]
        print("Angle: " + str(angle)  + " distance: " + str(distance_mm))
        if distance_mm <= 0:
            return -1
        return distance_mm
