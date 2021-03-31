import logging
import os
import threading
import time
from multiprocessing import Process


class Batch1:

    @staticmethod
    def run_sender(timeout):
        command = 'python3 Sender2.py 127.0.0.1 54321 sfile.jpg ' + str(timeout) + ' | tee -a output.txt'
        os.system(command)
        # with os.popen(command, "r") as p:
        #     r = p.read().strip('\n')
        #     logging.info(r)

    @staticmethod
    def run_receiver():
        os.system('python3 Receiver2.py 54321 rfile2.jpg')

    @staticmethod
    def run_both(timeout):
        for i in range(5):
            receiver = Process(target=Batch1.run_receiver)
            sender = Process(target=Batch1.run_sender, args=(timeout,))
            receiver.start()
            sender.start()
            receiver.join()
            sender.join()

            time.sleep(1)


# loopback settings
os.system('sudo tc qdisc del dev lo root')
os.system('sudo tc qdisc add dev lo root netem loss 5% delay 5ms rate 10mbit')
os.remove('output.txt')
print('run one')
# logging.basicConfig(level=logging.DEBUG, filename='Q1.log')
# logging.info('loss 5% delay 5ms rate 10mbit')

for j in (5, 10, 15, 20, 25, 30, 40, 50, 75, 100):
# for j in (25, 50, 75, 100, 125, 180, 200, 250, 375, 400):
    # logging.info('Retransmission timeout (ms) = ' + str(j))
    test = threading.Thread(target=Batch1.run_both, args=(j,))
    test.start()
    test.join()
    time.sleep(1)

# # loopback settings
# os.system('sudo tc qdisc del dev lo root')
# os.system('sudo tc qdisc add dev lo root netem loss 5% delay 25ms rate 10mbit')
# logging.basicConfig(level=logging.DEBUG, filename='Q1_25.log')
# logging.info('loss 5% delay 25ms rate 10mbit')
#
# for j in (5, 10, 15, 20, 25, 30, 40, 50, 75, 100):
#     logging.info('Retransmission timeout (ms) = ' + str(j))
#     test = threading.Thread(target=run_both, args=(j,))
#     test.start()
#     test.join()
#     time.sleep(1)


# # loopback settings
# os.system('sudo tc qdisc del dev lo root')
# os.system('sudo tc qdisc add dev lo root netem loss 5% delay 100ms rate 10mbit')
# logging.basicConfig(level=logging.DEBUG, filename='Q1_100.log')
# logging.info('loss 5% delay 100ms rate 10mbit')
#
# for j in (5, 10, 15, 20, 25, 30, 40, 50, 75, 100):
#     logging.info('Retransmission timeout (ms) = ' + str(j))
#     test = threading.Thread(target=run_both, args=(j,))
#     test.start()
#     test.join()
#     time.sleep(1)
