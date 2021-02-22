import sys
from socket import *


def read_file(filename):
    return open(filename, 'rb').read()


def file_to_packet(filedata):
    total_bytes = len(filedata)
    pac_size = 1024
    reminder = total_bytes % pac_size
    if reminder == 0:
        pac_num = int((total_bytes - reminder) / pac_size)
    else:
        pac_num = int(((total_bytes - reminder) / pac_size) + 1)
    pac_lis = []
    for i in range(pac_num):

        content = filedata[pac_size * i:pac_size * (i + 1)]
        pac_lis.append()
    return pac_lis


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_DGRAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    file_name = sys.argv[3]
    buf = 1027
    addr = (host, port)

    s.close()
