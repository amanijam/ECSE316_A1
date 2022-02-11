# Sending requests via sockets, and parsing the response

import socket
from packet import *

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
        header = Header() 

        # create Question
        question = Question(self.name, self.ty, 1)

        requestPack = Packet(header, question)
        addr = (self.server, self.port)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect(addr)
        client.send(requestPack.pack)
        data = client.recv(1024) ## NOTE: probably will have to loop or something to get full data
        return data
    
