# Sending requests via sockets, and parsing the response

import socket
from urllib import request 
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
        #create Header
        header = Header(0) # QR = 0

        # create Question
        qName = encodeName(self.name)
        qType = encodeType(self.ty)
        question = Question(qName, qType, '0x0001')

        requestPack = Packet(header, question)
        addr = (self.server, self.port)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sentto(bytes(requestPack), addr)
        data = client.recv(1024) # How is this data formatted..?
    
