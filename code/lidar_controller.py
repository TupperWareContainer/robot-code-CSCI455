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
        self.__lidar = RPLidar(lidar_port, timeout=timeout, baudrate=115200)
        self.__lidar_port = lidar_port
        self.__timeout = timeout 
        self.__max_distance = max_distance
        self.__stopScan = False
        self._scan_data = [0] * 360
        self._buffered_scan_data = [0] * 360
        self.__scan_thread = Thread(target = self.StartScan)
        self.__scan_thread.start()

    def StartScan(self):
        self.RebootLidar()
        started = False

        while not self.__stopScan:
            try:
                # iter_scans is a blocking generator
                for (new_scan, quality, angle, distance) in self.__lidar.iter_measurments(max_buf_meas=1000):
                    if new_scan:
                        started = True
                        self._scan_data[:] = self._buffered_scan_data  # Move the contents of the buffer to scan data
                        self._buffered_scan_data[:] = [0] * 360  # Reset the buffer
                        print("Moved data")

                    if not started:
                        # Skip the first partial lidar spin. This ensures that we only keep full spins!
                        continue

                    if distance == 0.0:
                        continue

                    idx = min([359, floor(angle)])
                    self._buffered_scan_data[idx] = distance # Write the distances to the buffer
            except RPLidarException as e:
                # This is where 'line length mismatch' is caught
                print(f"Lidar Hardware Error: {e}. Reconnecting...")
                self.RebootLidar()
            except Exception as e:
                print(f"Unexpected Exception: {e} ")
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
        distance_mm = self._scan_data[angle]
        return distance_mm
