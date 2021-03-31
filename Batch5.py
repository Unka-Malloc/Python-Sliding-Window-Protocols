import logging
import os
import threading
import time
from multiprocessing import Process


def run_sender(timeout, win_size, filename):
    command = 'python3 Sender4.py 127.0.0.1 54321 sfile.jpg ' + str(timeout) + ' ' + str(win_size) + filename
    os.system(command)


def run_receiver(win_size):
    os.system('python3 Receiver4.py 54321 rfile4.jpg ' + str(win_size))


def run_both(timeout, win_size, filename):
    for i in range(5):
        receiver = Process(target=run_receiver, args=(win_size,))
        sender = Process(target=run_sender, args=(timeout, win_size, filename))
        receiver.start()
        sender.start()
        receiver.join()
        sender.join()

        time.sleep(1)


if __name__ == '__main__':
    # loopback settings
    os.system('sudo tc qdisc del dev lo root')
    os.system('sudo tc qdisc add dev lo root netem loss 5% delay 25ms rate 10mbit')
    for j in (1, 2, 4, 8, 16, 32):
        test = threading.Thread(target=run_both, args=(55, j, ' | tee -a SR.txt'))
        test.start()
        test.join()
        time.sleep(1)
