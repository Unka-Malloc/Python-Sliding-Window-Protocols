import logging
import os
import threading
import time
from multiprocessing import Process

logging.basicConfig(level=logging.DEBUG, filename='Q3.log')


def run_sender(timeout, win_size, filename):
    command = 'python3 Sender3.py 127.0.0.1 55555 sfile.jpg ' + str(timeout) + ' ' + str(win_size) + filename
    os.system(command)
    # with os.popen(command, "r") as p:
    #     r = p.read()
    #     logging.info(r)


def run_receiver():
    os.system('python3 Receiver3.py 55555 rfile3.jpg')


def run_both(timeout, win_size, filename):
    for i in range(5):
        receiver = Process(target=run_receiver)
        sender = Process(target=run_sender, args=(timeout, win_size, filename))
        receiver.start()
        sender.start()
        receiver.join()
        sender.join()

        time.sleep(1)


# loopback settings
os.system('sudo tc qdisc del dev lo root')
os.system('sudo tc qdisc add dev lo root netem loss 5% delay 5ms rate 10mbit')
for j in (1, 2, 4, 8, 16, 32, 64, 128, 256):
    # logging.info('delay 5ms')
    # logging.info('Window Size = ' + str(j))
    # logging.info('Retransmission timeout (ms) = ' + str(timeout))
    test = threading.Thread(target=run_both, args=(15, j, ' | tee -a 5ms.txt'))
    test.start()
    test.join()
    time.sleep(1)

# loopback settings
os.system('sudo tc qdisc del dev lo root')
os.system('sudo tc qdisc add dev lo root netem loss 5% delay 25ms rate 10mbit')
for k in (1, 2, 4, 8, 16, 32, 64, 128, 256):
    # logging.info('delay 25ms')
    # logging.info('Window Size = ' + str(j))
    # logging.info('Retransmission timeout (ms) = ' + str(timeout))
    test = threading.Thread(target=run_both, args=(55, k, ' | tee -a 25ms.txt'))
    test.start()
    test.join()
    time.sleep(1)

# loopback settings
os.system('sudo tc qdisc del dev lo root')
os.system('sudo tc qdisc add dev lo root netem loss 5% delay 100ms rate 10mbit')
for l in (1, 2, 4, 8, 16, 32, 64, 128, 256):
    # logging.info('delay 100ms')
    # logging.info('Window Size = ' + str(j))
    # logging.info('Retransmission timeout (ms) = ' + str(timeout))
    test = threading.Thread(target=run_both, args=(205, l, ' | tee -a 100ms.txt'))
    test.start()
    test.join()
    time.sleep(1)
