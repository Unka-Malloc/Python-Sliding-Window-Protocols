import os
import threading


def run_1():
    os.system('python3 STRun.py')


def run_2():
    os.system('python3 SWRun.py')


def run_3():
    os.system('python3 GBNRun.py')


def run_4():
    os.system('python3 SRRun.py')


if __name__ == '__main__':
    t1 = threading.Thread(target=run_1)
    t1.start()
    t1.join()
    t2 = threading.Thread(target=run_2)
    t2.start()
    t2.join()
    t3 = threading.Thread(target=run_3)
    t3.start()
    t3.join()
    t4 = threading.Thread(target=run_4)
    t4.start()
    t4.join()
