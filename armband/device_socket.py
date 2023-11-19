from serial.tools.list_ports import comports
import time




class UsbCDC_socket():
    order = {500: b"\x55\x66\x52\x41\x54\x45\x01\x0A",
             1000: b"\x55\x66\x52\x41\x54\x45\x02\x0A",
             2000: b"\x55\x66\x52\x41\x54\x45\x03\x0A",
             'W': b"\x55\x66\x4D\x4F\x44\x45\x57\x0A",
             'Z': b"\x55\x66\x4D\x4F\x44\x45\x5A\x0A",
             'R': b"\x55\x66\x4D\x4F\x44\x45\x52\x0A",
             'B': b"\x55\x66\x42\x41\x54\x54\x42\x0A",
             'close': b"\x55\x66\x44\x49\x53\x43\x01\x0A",
             }

    @staticmethod
    def devce_list():
        return list(comports())

    def __init__(self, port) -> None:
        import serial
        self.__socket = serial.Serial(port=port)  # If a "port" is given, then the port will be opened immediately

    def connect_socket(self):
        # self.__socket.flushInput()
        self.__socket.write(self.order[500])
        time.sleep(0.1)
        self.__socket.read_all()

    def close_socket(self):
        self.__socket.write(self.order['R'])
        # self.__socket.write(self.order['close'])
        time.sleep(0.1)
        self.__socket.read_all()
        # self.__socket = None
        print('socket closed')

    def recv_socket(self, buffersize: int = 2048):
        return self.__socket.read(buffersize)

    # def start_impe(self):
    #     self.__socket.write(self.order['Z'])
    #     time.sleep(0.1)
    #     self.__socket.read(len(self.order['Z']))

    def start_data(self):
        # self.__socket.flushInput()
        self.__socket.write(self.order['W'])
        time.sleep(0.1)
        self.__socket.read(len(self.order['W']))

    def stop_recv(self):
        self.__socket.write(self.order['R'])
        time.sleep(0.1)
        self.__socket.read_all()

    def send_heartbeat(self):
        self.__socket.write(self.order['B'])
        time.sleep(0.1)
        ret = self.__socket.read(len(self.order['B']) + 1)
        print('batt raw', ret)
        battery = int(ret[-1])
        print('batt level:', battery)
        return battery
