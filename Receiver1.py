import sys
from socket import *

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_DGRAM)
    host = '127.0.0.1'
    port = int(sys.argv[1])
    file_name = sys.argv[2]
    buf = 1027
    addr = (host, port)

    s.bind((host, port))

    data, addr = s.recvfrom(buf)
    print("Received File:", data.strip())
    f = open(data.strip(), 'wb')

    data, addr = s.recvfrom(buf)
    try:
        while data:
            f.write(data)
            s.settimeout(2)
            data, addr = s.recvfrom(buf)
    except timeout:
        f.close()
        s.close()
        print("File Downloaded")
