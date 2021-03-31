import os
import threading


def run_Q1():
    os.system('python3 Batch1.py')


q1 = threading.Thread(target=run_Q1())
print('run batch1')
q1.start()
q1.join()

with open('output.txt',"r") as f:
    output = f.readlines()

ori_lis = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
txt_lis = []

for i in range(10):
    tmp_lis = output[i*5:i*5+5]
    retransmission = 0
    throughput = 0
    for j in tmp_lis:
        x = j.split(' ')
        retransmission += int(x[0])
        throughput += float(x[1].replace('\n', ''))
    txt_lis.append('Timeout {0}, Retransmission {1}, Throughput {2}'.format(ori_lis[i], retransmission/5, throughput/5))
for k in txt_lis:
    print(k)
