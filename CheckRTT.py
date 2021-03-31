import math
import re

with open('ping.txt', "r") as f:
    output = f.readlines()

SampleRTT = 50
EstimatedRTT = 50
DevRTT = 0
alpha = 0.125
beta = 0.25
count = 0


for i in output:
    if re.match('64 bytes', i) is not None:
        remove_time = re.split('time=', i)[1]
        remove_ms = re.split(' ms', str(remove_time))[0]
        SampleRTT = float(remove_ms)
        EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT
        DevRTT = (1 - beta) * DevRTT + beta * math.fabs(SampleRTT - EstimatedRTT)
        count += 1
Timeout = EstimatedRTT + 4 * DevRTT
print('Try {0}, Timeout {1}| EstimatedRTT = {2}, DevRTT = {3}'.format(count, Timeout, EstimatedRTT, DevRTT))

with open('ping100.txt', "r") as f:
    output = f.readlines()

SampleRTT = 200
EstimatedRTT = 200
count = 0


for i in output:
    if re.match('64 bytes', i) is not None:
        remove_time = re.split('time=', i)[1]
        remove_ms = re.split(' ms', str(remove_time))[0]
        SampleRTT = float(remove_ms)
        EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT
        DevRTT = (1 - beta) * DevRTT + beta * math.fabs(SampleRTT - EstimatedRTT)
        count += 1
Timeout = EstimatedRTT + 4 * DevRTT
print('Try {0}, Timeout {1}| EstimatedRTT = {2}, DevRTT = {3}'.format(count, Timeout, EstimatedRTT, DevRTT))


