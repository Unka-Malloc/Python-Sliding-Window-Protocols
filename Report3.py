import os
import threading


def run_Q3():
    os.system('python3 Batch3.py')


q3 = threading.Thread(target=run_Q3())
print('run batch3')
q3.start()
q3.join()

ori_lis = [1, 2, 4, 8, 16, 32, 64, 128, 256]
txt_lis = []

with open('5ms.txt', "r") as f:
    delay5 = f.readlines()

for i in range(len(ori_lis)):
    tmp_lis = delay5[i * 5:i * 5 + 5]
    retransmission = 0
    throughput = 0
    for j in tmp_lis:
        throughput += float(j.replace('\n', ''))
    txt_lis.append(
        'Window {0}, Throughput {1}'.format(ori_lis[i], throughput / 5))
print('Delay = 5ms')
for k in txt_lis:
    print(k)

with open('25ms.txt', "r") as f:
    delay25 = f.readlines()

for i in range(len(ori_lis)):
    tmp_lis = delay25[i * 5:i * 5 + 5]
    retransmission = 0
    throughput = 0
    for j in tmp_lis:
        throughput += float(j.replace('\n', ''))
    txt_lis.append(
        'Window {0}, Throughput {1}'.format(ori_lis[i], throughput / 5))
print('Delay = 25ms')
for k in txt_lis:
    print(k)

with open('100ms.txt', "r") as f:
    delay100 = f.readlines()

for i in range(len(ori_lis)):
    tmp_lis = delay100[i * 5:i * 5 + 5]
    retransmission = 0
    throughput = 0
    for j in tmp_lis:
        throughput += float(j.replace('\n', ''))
    txt_lis.append(
        'Window {0}, Throughput {1}'.format(ori_lis[i], throughput / 5))
print('Delay = 100ms')
for k in txt_lis:
    print(k)
