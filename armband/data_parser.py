import re, traceback
from datetime import datetime

class Parser:
    HOTKEY_TRIGGER = -2
    BATTERY = -1

    def __init__(self, num_channels, fs):
        self.num_channels = num_channels
        self.ch_bytes = 3
        self.scale_ratio = 0.02235174
        self.__buffer = b""
        self.__last_num = 255

        self.__start = 2
        self.__checksum = -4
        self.__trigger = -3
        self.__battery = -2
        self.__packet = -1
        self.packet_drop_count = 0
        length = self.num_channels * self.ch_bytes + abs(self.__checksum)
        # 正则表达式
        self.__pattern = re.compile(b"\xbb\xaa.{%d}" % length, flags=re.DOTALL)

    def clear_buffer(self):
        self.__buffer = b""
        self.__last_num = 255
        self.packet_drop_count = 0

    def parse_data(self, q: bytes) -> list[list[int]]:
        self.__buffer += q
        frame_list: list[bytes] = self.__pattern.findall(self.__buffer)
        self.__buffer = self.__pattern.split(self.__buffer)[-1]
        data_list = []

        for frame in frame_list:
            raw = frame[self.__start : self.__checksum]
            if frame[self.__checksum] != (~sum(raw)) & 0xFF:
                print(
                    "|Checksum invalid, last vailid",
                    cur_num,
                    " drop packet",
                    datetime.now(),
                    "\n|Current:",
                    frame.hex(),
                )
                continue
            cur_num = frame[self.__packet]
            if cur_num != ((self.__last_num + 1) % 256):
                self.packet_drop_count += 1
                print(
                    ">>>> Pkt Los Cur:",
                    cur_num,
                    "Last valid:",
                    self.__last_num,
                    "buf len:",
                    len(self.__buffer),
                    datetime.now(),
                    "<<<<\n",
                )
            self.__last_num = cur_num
            # raw=self.enc_data(raw) # decrypt data if needed
            data = [
                int.from_bytes(raw[i : i + self.ch_bytes], signed=True)
                for i in range(0, len(raw), self.ch_bytes)
            ]  # default byteorder="big", fill 1 byte to 4 bytes signed int
            data.append(frame[self.__trigger])
            data.append(0)  # sys debug info
            data.append(frame[self.__battery])
            data_list.append(data)
        return data_list
