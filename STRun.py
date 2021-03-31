import os
import threading
import time
from multiprocessing.dummy import Process


def run_sender():
    os.system('python3 Sender1.py 127.0.0.1 55555 sfile.jpg')


def run_receiver():
    os.system('python3 Receiver1.py 55555 rfile1.jpg')


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
    os.system('sudo tc qdisc add dev lo root netem loss 0% delay 5ms rate 10mbit')
    test = threading.Thread(target=run_both)
    test.start()
    test.join()
    print('Sender/Receiver 1 Stress Testing: Success')
