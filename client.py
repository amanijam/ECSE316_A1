import socket
import sys
localIP = "127.0.0.1"
localPort = 20001
sock_send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock_recv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#sock_recv.bind((localIP, localPort))
sock_send.connect(('www.google.com', 53))  
#sock.sendto(b"hello", (localIP, localPort))
#sock.bind((socket.gethostbyname('www.google.com'), localPort))
#sock.sendto(b"hello")
msg = "hello"
sock_send.send(msg.encode())
sock_send.recv(128)
#print(sock_recv.recvfrom(1024))