import os
import threading

print('run batch5')


def run_Q5():
    os.system('python3 Batch5.py')


if __name__ == '__main__':
    q5 = threading.Thread(target=run_Q5())
    q5.start()
    q5.join()

    ori_lis = [1, 2, 4, 8, 16, 32]
    txt_lis = []

    with open('SR.txt', "r") as f:
        SR = f.readlines()

    for i in range(len(ori_lis)):
        tmp_lis = SR[i * 5:i * 5 + 5]
        throughput = 0
        for j in tmp_lis:
            throughput += float(j.replace('\n', ''))
        txt_lis.append('Window {0}, Throughput {1}'.format(ori_lis[i], throughput / 5))
    print('Delay = 25ms, timeout = 55ms')
    for k in txt_lis:
        print(k)
