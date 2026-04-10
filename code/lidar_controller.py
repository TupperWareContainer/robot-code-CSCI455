from rplidar import RPLidar, RPLidarException
from math import floor
from threading import Thread
import threading
import time

class LidarController:
    __lidar : RPLidar
    __max_distance : float
    __scan_thread : Thread
    __stopScan : bool
    __lidar_port : str 
    __timeout : float

    def __init__(self, lidar_port : str, timeout : float, max_distance : float):
        self.__lidar = RPLidar(lidar_port, timeout=timeout)
        self.__lidar_port = lidar_port
        self.__timeout = timeout 
        self.__max_distance = max_distance
        self.__stopScan = False
        self._scan_data = [0] * 360
        #self._scan_timestamps = [0.0] * 360
        #self._data_lock = threading.Lock()
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

        while not self.__stopScan:
            print("scanning") 
            try:
                # iter_scans is a blocking generator
                for scan in self.__lidar.iter_scans():
                    for (_, angle, distance) in scan:

                        #with self._data_lock:
                        if distance != 0:
                            idx = min([359, floor(angle)])
                            self._scan_data[idx] = distance
                    
                      # Yields control to other threads
                    #self.__lidar.clear_input()
            except RPLidarException as e:
                # This is where 'line length mismatch' is caught
                print(f"Lidar Hardware Error: {e}. Reconnecting...")
                self.RebootLidar()
            except Exception as e:
                print("Unexpected Exception...")
                self.RebootLidar()

    def RebootLidar(self):
        try:
            self.__lidar.stop()
            self.__lidar.disconnect()
            self.__lidar.connect()
            self.__lidar.clear_input()
        except Exception as e:
            print(f"Could not reset lidar: {e}")

    def StopScan(self):
        self.__stopScan = True
        self.__scan_thread.join()

    def GetDistanceMM(self, angle : int):
        #with self._data_lock:
        distance_mm = self._scan_data[angle]
        return distance_mm
