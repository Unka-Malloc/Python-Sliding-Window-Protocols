# /* Yizhuo Yang s1800825 */
import threading
import time
import sys
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from socket import *

from Sender3 import Sender3


class Sender4(Sender3):
    def __init__(self, host, port, file_name, timeout, win_size):
        super(Sender4, self).__init__(host, port, file_name, timeout, win_size)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        # not in window == True : ack yes, in window == True : ack not
        self.unused = []
        self.window = []
        self.finished = []
        self.ack = threading.Condition()

    def send_one(self, pkt):
        e = threading.Event()
        self.sock.sendto(self.pac_lis[pkt], self.dst_addr)
        check = threading.Thread(target=self.check_one, args=(pkt, e))
        check.setDaemon(True)
        check.start()
        while True:
            if not e.wait(timeout=self.timeout):
                self.sock.sendto(self.pac_lis[pkt], self.dst_addr)
                # print('resend pkt {}'.format(pkt))
            else:
                break
        self.finished.append(pkt)
        # print('pkt {} finished'.format(pkt))

    def check_one(self, pkt, e: threading.Event):
        while True:
            with self.mutex:
                if pkt not in self.window:
                    e.set()
            beta = 0.25
            time.sleep(self.timeout * beta)

    def recv_all(self):
        buffer = 2
        while True:
            ack_b, addr = self.sock.recvfrom(buffer)
            ack = int.from_bytes(ack_b, 'big')
            # print('recv pkt {0}'.format(ack))

            with self.mutex:
                if self.send_base <= ack <= self.send_base + self.win_size - 1:
                    if ack in self.window:
                        self.window.remove(ack)
                        self.window.sort()
                        if ack == self.send_base:
                            if len(self.window) == 0:
                                self.send_base = self.next_seq
                            else:
                                self.send_base = self.window[0]
                            # forward w
                            for i in range(self.win_size):
                                if self.next_seq < self.send_base + self.win_size:
                                    self.window.append(self.next_seq)
                                    self.window.sort()
                                    self.unused.append(self.next_seq)
                                    self.unused.sort()
                                    self.next_seq += 1
            # print('window {0}'.format(self.window))
            # print('base_next {0} : {1}'.format(self.send_base, self.next_seq))

    def send_file(self):
        time_start = float(time.perf_counter())
        recv = threading.Thread(target=self.recv_all)
        recv.setDaemon(True)
        recv.start()

        with self.mutex:
            for i in range(self.win_size):
                if self.next_seq < self.send_base + self.win_size:
                    self.window.append(i)
                    self.unused.append(i)
                    self.window.sort()
                    self.unused.sort()
                    self.next_seq += 1

        with ThreadPoolExecutor(max_workers=self.win_size) as pool:
            while True:
                if len(self.pac_lis) - 1 in self.finished and len(self.finished) == len(self.pac_lis):
                    break
                if len(self.unused) > 0:
                    with self.mutex:
                        for j in self.unused:
                            pool.submit(self.send_one, j)
                            self.unused.remove(j)
                alpha = 0.125
                time.sleep(self.timeout * alpha)
        # print(len(self.finished))
        time_end = float(time.perf_counter())
        total_bytes = self.get_size()
        print((total_bytes/1000)/(time_end - time_start))


if __name__ == '__main__':
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    FILE_NAME = sys.argv[3]
    TIMEOUT = sys.argv[4]
    WIN_SIZE = sys.argv[5]

    logging.basicConfig(level=logging.INFO, filename='sender4.log')

    sender4 = Sender4(HOST, PORT, FILE_NAME, TIMEOUT, WIN_SIZE)
    sender4.send_file()
