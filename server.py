import socket
import sys

#server = socket.gethostbyname(socket.gethostname())
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.gethostbyname(sys.argv[1])
print(ip)
sock.bind((localIP, localPort))
while True:
    print("waiting")
    data, addr = sock.recvfrom(1024)
    print(data)


#print(ip)