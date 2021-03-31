# /* Yizhuo Yang s1800825 */
import sys
from socket import *


class Receiver:
    def __init__(self, port, file_name):
        self.host = '127.0.0.1'
        self.port = port
        self.file_name = file_name
        self.buffer = 1027

    @staticmethod
    def get_seq(packet):
        seq = packet[0:2]
        return int.from_bytes(seq, 'big')

    @staticmethod
    def get_seq_b(packet):
        return packet[0:2]

    @staticmethod
    def get_eof(packet):
        return packet[2]

    @staticmethod
    def remove_header(packet):
        return packet[3:]

    @staticmethod
    def receive_data(port, buffer):
        localhost = '127.0.0.1'
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind((localhost, port))
        data, addr = s.recvfrom(buffer)
        s.close()
        return data, addr

    def receive_file(self):
        content = bytes(0)
        # print('Start')
        file = open(self.file_name, 'wb')
        while True:
            data, addr = Receiver.receive_data(self.port, self.buffer)
            # print(self.get_seq(data))
            content += self.remove_header(data)
            if self.get_eof(data) == 1 or not data:
                break
        file.write(content)
        # print('End', len(content))


if __name__ == '__main__':
    PORT = int(sys.argv[1])
    FILE_NAME = sys.argv[2]

    receiver = Receiver(PORT, FILE_NAME)
    receiver.receive_file()
