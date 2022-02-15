# Sending requests via sockets and receiving response. Calls classes and functions
#   in other files to perform decoding and parsing of response. 

import socket
from packet import *
from packet_decoding import Packet_Decoder

class Query:
    def __init__(self, server, name, timeout=5, maxR=3, port=53, ty='A'):
        self.timeout = timeout  # Default: 5s
        self.maxR = maxR        # Default: 3 retries
        self.port = port        # Default: port 53
        self.ty = ty            # Default: type A
        self.server = server
        self.name = name
        
    def send(self):
        self.header = Header()  #create Header for request

        question = Question(self.name, self.ty, 1)  # create Question

        requestPack = Packet(self.header, question) # generate request packet

        # Create and send socket
        addr = (self.server, self.port)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect(addr)
        client.settimeout(self.timeout)
        client.send(requestPack.pack)

        # Receive data 
        try:
            data = client.recv(1024)
        except: 
            return [6, None] # timeout exception
        
        decoder = Packet_Decoder(data, self.header.id)
        code_val, response = decoder.decode_packet()
        return [code_val, response]
    
