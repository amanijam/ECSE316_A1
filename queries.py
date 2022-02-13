# Sending requests via sockets, and parsing the response

import socket
import timeit
from packet import *
import timeit

class Query:
    def __init__(self, server, name, timeout=5, maxR=3, port=53, ty='A'):
        self.timeout = timeout
        self.maxR = maxR
        self.port = port
        self.ty = ty
        self.server = server
        self.name = name
        
    def send(self):
        #create Header for request
        self.header = Header() 

        # create Question
        question = Question(self.name, self.ty, 1)

        requestPack = Packet(self.header, question)
        addr = (self.server, self.port)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect(addr)
        client.settimeout(self.timeout)
        client.send(requestPack.pack)
        #print("Request pack: {}".format(requestPack.pack))
        try:
            data = client.recv(1024)
        except socket.timeout:
            return 6
        return data
    
