# /* Yizhuo Yang s1800825 */
import logging
import sys
from socket import *

from Receiver3 import Receiver3


class Receiver4(Receiver3):
    def __init__(self, port, file_name, win_size):
        super(Receiver4, self).__init__(port, file_name)
        self.win_size = int(win_size)

    def receive_file(self):
        window = {}
        content = bytes(0)
        recv_base = 0
        localhost = '127.0.0.1'
        s = socket(AF_INET, SOCK_DGRAM)
        s.settimeout(3)
        s.bind((localhost, self.port))
        while True:
            try:
                data, addr = s.recvfrom(self.buffer)
            except timeout:
                break
            seq = self.get_seq(data)
            seq_b = seq.to_bytes(2, 'big')
            # in window
            if recv_base <= seq <= recv_base + self.win_size - 1:
                s.sendto(seq_b, addr)
                # print('ack {0}, recv_base {1}'.format(seq, recv_base))
                window[seq] = self.remove_header(data)
                if seq == recv_base:
                    content += self.remove_header(data)
                    del window[seq]
                    recv_base += 1
                    # forward window
                    del_lis = []
                    key_lis = list(window.keys())
                    key_lis.sort()
                    for i in key_lis:
                        if i == recv_base:
                            del_lis.append(recv_base)
                            content += window[i]
                            recv_base += 1
                    for j in del_lis:
                        del window[j]
                    # last packet
            # in last window
            elif recv_base - self.win_size <= seq <= recv_base - 1:
                s.sendto(seq_b, addr)
                # print('ack {0}, recv_base {1}'.format(seq, recv_base))
            if self.get_eof(data) == 1 and len(window) == 0:
                while True:
                    try:
                        data, addr = s.recvfrom(self.buffer)
                        seq = self.get_seq(data)
                        seq_b = seq.to_bytes(2, 'big')
                        s.sendto(seq_b, addr)
                    except timeout:
                        break
                break
        s.close()
        file = open(self.file_name, 'wb')
        file.write(content)


if __name__ == '__main__':
    PORT = int(sys.argv[1])
    FILE_NAME = sys.argv[2]
    WIN_SIZE = sys.argv[3]

    # logging.basicConfig(level=logging.INFO, filename='receiver4.log')

    receiver = Receiver4(PORT, FILE_NAME, WIN_SIZE)
    receiver.receive_file()
