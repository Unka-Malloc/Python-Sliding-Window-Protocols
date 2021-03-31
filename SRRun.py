import os
import threading
import time
from multiprocessing.dummy import Process


def run_sender():
    os.system('python3 Sender4.py 127.0.0.1 55555 sfile.jpg 55 32')


def run_receiver():
    os.system('python3 Receiver4.py 55555 rfile4.jpg 32')


def run_both():
    run = 20
    for i in range(run):
        receiver = Process(target=run_receiver)
        sender = Process(target=run_sender)
        receiver.start()
        sender.start()
        receiver.join()
        sender.join()

        time.sleep(1)


if __name__ == '__main__':
    os.system('sudo tc qdisc del dev lo root')
    os.system('sudo tc qdisc add dev lo root netem loss 5% delay 25ms rate 10mbit')
    test = threading.Thread(target=run_both)
    test.start()
    test.join()
    print('Sender/Receiver 4 Stress Testing: Success')
