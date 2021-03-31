# /* Yizhuo Yang s1800825 */
import threading
import time

from Sender2 import Sender2
from socket import *
import sys
import logging


class Sender3(Sender2):
    # extend sender2
    def __init__(self, host, port, file_name, timeout, win_size):
        super(Sender3, self).__init__(host, port, file_name, timeout)
        self.win_size = int(win_size)
        self.dst_addr = (self.host, self.port)
        self.pac_lis = self.add_header(self.file_to_packet(self.read_file(self.file_name)))
        self.send_base = 0
        self.next_seq = 0
        self.mutex = threading.Lock()

    def send_window(self, s: socket, e: threading.Event):
        while True:
            if self.send_base > len(self.pac_lis) - 1 or self.next_seq > len(self.pac_lis) - 1:
                break
            if self.next_seq < self.send_base + self.win_size:
                for i in range(self.win_size):
                    s.sendto(self.pac_lis[self.next_seq], self.dst_addr)

                    with self.mutex:
                        self.next_seq += 1

                    if self.next_seq >= len(self.pac_lis) - 1:
                        with self.mutex:
                            self.next_seq = len(self.pac_lis) - 1
                        break
                logging.debug('ReBuild Window {0}'.format(list(range(self.send_base, self.next_seq))))
            e.clear()
            logging.debug('Wait')
            if not e.wait(self.timeout):
                logging.debug('Timeout detected')
                for i in range(self.send_base, self.next_seq):
                    s.sendto(self.pac_lis[i], self.dst_addr)
                    logging.debug('ReSend pkt {0}'.format(i))

    def recv_ack(self, s: socket, e: threading.Event):
        buffer = 2
        while True:
            ack_b, addr = s.recvfrom(buffer)
            ack = int.from_bytes(ack_b, 'big')
            logging.debug('recv ack {0}'.format(ack))

            with self.mutex:
                if ack == self.send_base:
                    if not self.next_seq > len(self.pac_lis) - 1:
                        s.sendto(self.pac_lis[self.next_seq], self.dst_addr)
                    self.send_base += 1
                    if self.next_seq < len(self.pac_lis) - 1:
                        self.next_seq += 1
                    logging.debug('Forward Window {0}'.format(list(range(self.send_base, self.next_seq))))
                    e.set()
                elif ack > self.send_base:
                    self.send_base = ack + 1
                    self.next_seq = self.send_base
                    logging.debug('Reset Window {0}'.format(list(range(self.send_base, self.next_seq))))
                    e.set()

            if ack == len(self.pac_lis) - 1:
                break

    def send_file(self):
        time_start = float(time.perf_counter())

        s = socket(AF_INET, SOCK_DGRAM)

        acked = threading.Event()

        send = threading.Thread(target=self.send_window, args=(s, acked))
        recv = threading.Thread(target=self.recv_ack, args=(s, acked))

        send.setDaemon(True)
        recv.setDaemon(True)

        send.start()
        recv.start()

        send.join()
        recv.join()

        time_end = float(time.perf_counter())
        total_bytes = self.get_size()
        print((total_bytes / 1000) / (time_end - time_start))
        logging.debug('Main Thread Close')


if __name__ == '__main__':
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    FILE_NAME = sys.argv[3]
    TIMEOUT = sys.argv[4]
    WIN_SIZE = sys.argv[5]

    logging.basicConfig(level=logging.INFO, filename='sender3.log')

    sender3 = Sender3(HOST, PORT, FILE_NAME, TIMEOUT, WIN_SIZE)
    sender3.send_file()
