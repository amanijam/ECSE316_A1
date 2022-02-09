# Putting together the packets, which are made up of the Header and the Question (2 classes?)

import random

class Packet:
    # Header, Question, Answer, Authority, Additional
    def __init__(self, header, question, answer=None, auth=None, add=None):
        self.header = header
        self.question = question

## NOTE: So far, only for REQUESTS ##
class Header:
    # ID      : 16-bit              ; should be random
    # QR      : 1-bit               ; query (0) or response (1)
    # Opcode  : 4-bit               ; should be 0, representing standard query
    # AA      : 1-bit               ; for responses, whether (1) or not (0) the name server is an authority 
    # TC      : 1-bit               ; whether (1) or not (0) message was truncated
    # RD      : 1-bit               ; set to 1 to indicate we desire recursion
    # RA      : 1-bit               ; ?
    # Z       : 3-bit               ; set to 0
    # RCODE   : 4-bit               ; response code (set to 0 for request messages)
    #               0 No error condition
    #               1 Format error: name server was unable to interpret the query
    #               2 Server failure: name server was unable to process this query due to a problem with the name server
    #               3 Name error: meaningful only for responses from an authoritative name server, this code
    #                               signifies that the domain name referenced in the query does not exist
    #               4 Not implemented: name server does not support the requested kind of query
    #               5 Refused: the name server refuses to perform the requested operation for policy reasons
    # QDCOUNT : 16-bit              ; num of entries in question section (set to 1)
    # ANCOUNT : 16-bit              ; num of resource records in the answer section
    # NSCOUNT : 16-bit              ; num of name server recors in Authority section (can ignore)
    # ARCOUNT : 16-bit              ; num of records in Additional section
    def __init__(self):
        self.id = random.getrandbits(16) # returns a non-negative integer with k random bits
        self.qr = 0
        self.opcode = 0
        self.aa = 0
        self.tc = 0
        self.rd = 1
        self.ra = 0
        self.z = 0
        self.rcode = 0
        self.qdcount = 1
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0
        

class Question:
    # QNAME  : domain name represented by sequence of labels
    # QTYPE  : 16-bit code specifying type of query 
                # 0x0001 for type-A
                # 0x0002 for type-NS
                # 0x000f for type-MX
    # QCLASS : 16-bit code specifying class of query (should always be 0x0001, representing an Internet address)

    # Expected inputs: name (str), ty (str), class (int) 
    def __init__(self, name, ty, c: int):
        self.qName = encodeName(name)
        self.qType = encodeType(ty)
        self.qClass = c.to_bytes(16, 'big')

def encodeName(name):
    lengths = []
    count = 0
    for i in range(0, len(name)):
        if(name[i] == '.'):
            lengths.append(count)
            count = 0
        else:
            count += 1
    lastI = 0
    for i in range(0, len(lengths)): lastI += (lengths[i] + 1)
    lastLength = len(name) - lastI
    lengths.append(lastLength)
    return lengths


def encodeType(ty):
    return ty

    