import re, traceback
from datetime import datetime
import numpy as np
import math

# from gmssl import Sm4


class Parser:
    HOTKEY_TRIGGER = -2
    BATTERY = -1

    def __init__(self, num_channels, fs):
        self.imp_len = 1024 * fs / 500
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

        # ekey = b"\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10"
        # self.enc = Sm4(ekey, encrypt=False)
        # length = math.ceil(self.num_channels * self.ch_bytes / len(ekey))
        # * len( ekey) + abs(self.__checksum)
        self.__pattern = re.compile(b"\xbb\xaa.{%d}" % length, flags=re.DOTALL)

    # def enc_data(self, raw):
    #     en = b""
    #     for i in range(0, len(raw), 16):
    #         en += self.enc.encrypt(raw[i : i + 16])
    #     return en

    def clear_buffer(self):
        self.__buffer = b""
        self.__last_num = 255
        self.packet_drop_count = 0

    def get_impedance(self, impe_queue):
        data = np.array(impe_queue)
        iserror = np.sum(np.absolute(data) <= 4000000, axis=0) / self.imp_len
        freq_data = np.fft.fft(data, axis=0)
        factor = 1000 / 512 * self.scale_ratio / 6
        tt = np.max(np.absolute(freq_data[62:67]), axis=0)
        impe_data = list((tt * factor * math.pi / 4 - 5000).astype(int))
        for i,val in enumerate(iserror):
            if val <= 0.2:
                impe_data[i] = 1000000
        return impe_data

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
