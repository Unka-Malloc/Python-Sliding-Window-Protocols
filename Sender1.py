# /* Yizhuo Yang s1800825 */
import sys
import time
from socket import *


class Sender:
    def __init__(self, host, port, file_name=''):
        self.host = host
        self.port = port
        self.file_name = file_name

    @staticmethod
    def read_file(filename):
        return open(filename, 'rb').read()

    @staticmethod
    def file_to_packet(file_data):
        total_bytes = len(file_data)
        pac_size = 1024
        reminder = total_bytes % pac_size
        if reminder == 0:
            pac_num = int((total_bytes - reminder) / pac_size)
        else:
            pac_num = int(((total_bytes - reminder) / pac_size) + 1)
        packets = []
        for i in range(pac_num):
            content = file_data[pac_size * i:pac_size * (i + 1)]
            packets.append(content)
        return packets

    @staticmethod
    def add_header(packets):
        for i in range(len(packets)):
            seq = i
            seq_b = seq.to_bytes(2, 'big')
            if i == len(packets) - 1:
                eof = 1
            else:
                eof = 0
            eof_b = eof.to_bytes(1, 'big')
            header = seq_b + eof_b
            packets[i] = header + packets[i]
        return packets

    @staticmethod
    def send_data(host, port, data):
        s = socket(AF_INET, SOCK_DGRAM)
        addr = (host, port)
        s.connect(addr)
        s.sendto(data, addr)
        s.close()

    def send_file(self):
        file_data = self.read_file(self.file_name)
        pac_lis = self.add_header(self.file_to_packet(file_data))

        for i in range(len(pac_lis)):
            self.send_data(self.host, self.port, pac_lis[i])
            time.sleep(0.02)


if __name__ == '__main__':
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    FILE_NAME = sys.argv[3]

    sender = Sender(HOST, PORT, FILE_NAME)
    sender.send_file()
