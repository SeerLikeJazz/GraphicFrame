import time, traceback
from multiprocessing import Process, Queue, Value
import queue
from .device_socket import UsbCDC_socket as device_socket

CAP_SIGNAL = 10
CAP_SIGNAL_START = 11
CAP_IDLE = 30
CAP_IDLE_START = 31
CAP_END = 101
CAP_TERMINATED = 102


class MyDevice(Process):
    def __init__(self, port, socket_flag: Value):
        print("initing iRecorder")
        Process.__init__(self, daemon=True)
        self.socket_flag = socket_flag
        self.__raw_data = Queue(5000)
        self.__cap_status = Value("i", CAP_TERMINATED)
        self.__battery = Value("i", -1)
        self.port = port

    @staticmethod
    def get_device():
        devices = device_socket.devce_list()
        return devices
        # for device in devices:
        #     if (device.pid == 22336) and (device.vid == 1155):
        #         return device.description
        # return None

    def get_data(self):
        data = []
        try:
            while not self.__raw_data.empty():
                temp = self.__raw_data.get(block=False)
                data.append(temp)
        except queue.Empty:
            pass
        except Exception:
            traceback.print_exc()
        return data  # (channels, length)

    def start_acquisition_data(self):
        if self.__cap_status.value == CAP_TERMINATED:
            return
        self.__cap_status.value = CAP_SIGNAL_START
        while self.__cap_status.value != CAP_SIGNAL:
            continue

    def stop_acquisition(self):
        if self.__cap_status.value == CAP_TERMINATED:
            return
        self.__cap_status.value = CAP_IDLE_START
        while self.__cap_status.value != CAP_IDLE:
            continue

    def close_cap(self):
        if self.__cap_status.value == CAP_TERMINATED:
            return
        # ensure socket is closed correctly
        self.__cap_status.value = CAP_END
        while self.__cap_status.value != CAP_TERMINATED:
            time.sleep(0.05)

    def get_battery_value(self):
        return self.__battery.value

    def socket_recv(self):
        while self.__ThreadSwitch_of_socket_recv:
            try:
                data = self.__socket.recv_socket()
                if len(data) != 0:
                    self.__recv_queue.put(data)
                else:
                    time.sleep(0.01)
            except:
                print("damn")
                time.sleep(0.2)
                traceback.print_exc()

    def run(self):
        from .data_parser import Parser
        import threading

        self.socket_flag.value = 1
        self.__socket = device_socket(self.port) # 打开了串口
        try:
            self.__socket.connect_socket()
            self.__socket.stop_recv()
            self.__battery.value = self.__socket.send_heartbeat()
        except Exception:
            self.socket_flag.value = 4
            self.__socket.close_socket()
            return

        self.sys_data = 0
        self.__timestamp = time.time()
        self.__recv_queue = queue.Queue()
        self.__cap_status.value = CAP_IDLE_START
        self.__parser = Parser(32,500)
        self.__ThreadSwitch_of_socket_recv = False
        self.__recv_thread = threading.Thread(target=self.socket_recv, daemon=True)
        self.__recv_thread.start()
        # self.socket_flag.value = 2
        while True:
            if self.__cap_status.value == CAP_SIGNAL_START:
                print("CAP_SIGNAL_START")
                self.__parser.clear_buffer()
                while not self.__raw_data.empty():
                    try:
                        self.__raw_data.get(block=False)
                    except queue.Empty:
                        print("Process queue bug caught")
                while not self.__recv_queue.empty():
                    try:
                        self.__recv_queue.get(block=False)
                    except queue.Empty:
                        print("Thread queue bug caught")
                try:
                    self.__ThreadSwitch_of_socket_recv = True  # 线程打开前，while循环先打开
                    self.__recv_thread = threading.Thread(target=self.socket_recv, daemon=True)
                    self.__recv_thread.start() # 打开线程
                    self.__socket.start_data()
                    self.__cap_status.value = CAP_SIGNAL
                    self.__timestamp = time.time()
                except:
                    traceback.print_exc()
                    self.socket_flag.value = 6
                    self.__cap_status.value = CAP_END
            elif self.__cap_status.value == CAP_SIGNAL:
                try:
                    data = self.__recv_queue.get(timeout=0.02)
                    data_list = self.__parser.parse_data(data)
                    if len(data_list) < 1:
                        continue
                    self.__timestamp = time.time()
                    for data in data_list:
                        data[Parser.HOTKEY_TRIGGER] = self.sys_data
                        self.sys_data = 0
                        self.__battery.value = data[Parser.BATTERY]
                        self.__raw_data.put(
                            data[0 : Parser.BATTERY], block=False
                        )  # assure complete collection
                except queue.Full:
                    print(">>>queue full<<<")
                    self.socket_flag.value = 9
                    self.__cap_status.value = CAP_END
                except:
                    if (time.time() - self.__timestamp) > 4:
                        self.socket_flag.value = 3
                        self.__cap_status.value = CAP_END

            elif self.__cap_status.value == CAP_IDLE_START:
                try:
                    print("CAP_IDLE_START")
                    print("DROPPED PACKETS COUNT:", self.__parser.packet_drop_count)
                    self.__ThreadSwitch_of_socket_recv = False
                    self.__recv_thread.join()
                    print("joined")
                    self.__socket.stop_recv()
                    self.__cap_status.value = CAP_IDLE
                    self.__timestamp = time.time()
                except:
                    traceback.print_exc()
                    self.socket_flag.value = 6
                    self.__cap_status.value = CAP_END
            elif self.__cap_status.value == CAP_IDLE:
                time.sleep(0.1)
                self.socket_flag.value = 2
                if (time.time() - self.__timestamp) > 5:
                    try:
                        self.__battery.value = self.__socket.send_heartbeat()
                        # heartbeat to keep socket alive
                        self.__timestamp = time.time()
                        print(">>>Stayin' alive, stayin' alive")
                    except:
                        traceback.print_exc()
                        self.socket_flag.value = 5
                        self.__cap_status.value = CAP_END
            elif self.__cap_status.value == CAP_END:
                print("CAP_END")
                self.__ThreadSwitch_of_socket_recv = False
                time.sleep(0.1)
                try:
                    self.__socket.stop_recv()
                except:
                    traceback.print_exc()
                self.__socket.close_socket()
                self.__cap_status.value = CAP_TERMINATED
                print("CAP_TERMINATED")
                return
            else:
                print("shared value bug, but it's ok")
