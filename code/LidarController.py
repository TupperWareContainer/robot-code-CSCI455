from serial import SerialException
from rplidar import RPLidar, RPLidarException
from math import floor
from threading import Thread
import time

class LidarController:
    __lidar : RPLidar
    __max_distance : float
    __scan_thread : Thread
    __stopScan : bool
    def __init__(self, lidar_port : str, timeout : float, max_distance : float):
        self.__lidar = RPLidar(lidar_port, baudrate=115200, timeout=timeout)
        self.__max_distance = max_distance
        self.__stopScan = False
        self.__scan_thread = Thread(target = self.StartScan)
        self.__scan_thread.start()
        self.__scan_data = [0.0] * 360

    def StartScan(self):
        try:
            print("Cleaning up Lidar state")
            self.__lidar.stop()
            self.__lidar.disconnect()
            self.__lidar.connect()
            self.__lidar.clear_input()
        except Exception as e:
            print(f"Unexpected Error: {e}")

        while not self.__stopScan:
            try:
                # iter_scans is a blocking generator
                for scan in self.__lidar.iter_scans():
                    for point in scan:
                        quality, angle, distance = point
                        idx = min([359, int(floor(angle))])
                        self.__scan_data[idx] = distance

                    time.sleep(0.1)  # Yields control to other threads
            except RPLidarException as e:
                # This is where 'line length mismatch' is caught
                print(f"Lidar Hardware Error: {e}. Reconnecting...")
                self.__lidar.disconnect()  # Essential to drop the bad connection
                self.__lidar.connect()  # Restart the serial sync
            except SerialException:
                self.__lidar.stop()
                self.__lidar.disconnect()
                self.__lidar = RPLidar(self.__port)

        self.__lidar.stop()
        self.__lidar.disconnect()

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
        distance_mm = self.__scan_data[clean_angle]

        if distance_mm <= 0 or distance_mm > self.__max_distance:
            return -1
        return distance_mm