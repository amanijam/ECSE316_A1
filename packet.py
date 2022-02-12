# Putting together the packets, which are made up of the Header and the Question (2 classes?)

import random

class Packet:
    # Header, Question, Answer, Authority, Additional
    def __init__(self, header=None, question=None, answer=None, auth=None, add=None):
        self.pack = b''
        if(header != None): 
            self.pack = b''.join([self.pack, header.getSection()])
            if(question != None):
                self.pack = b''.join([self.pack, question.getSection()])

    
    ## NOTE: Sections should be added in order! ##
    ## ASSUMPTION: Arg 'c' has a method called getSection()
        # which returns the entire section as a bytes object
    def addSection(self, c):
        self.pack = b''.join([self.pack, c.getSection()])
        return self.pack

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

    ## NOTE (IMPORTANT): Only for REQUESTS (so far) ##
    def __init__(self):
        id = random.getrandbits(16) # returns a non-negative integer with k random bits
        self.id = id.to_bytes(2, 'big')
        self.flags = b'\x01\x00'
        self.qdcount = b'\x00\x01'
        self.ancount = b'\x00\x00'
        self.nscount = b'\x00\x00'
        self.arcount = b'\x00\x00'

    def getSection(self):
        return b''.join([self.id, self.flags, self.qdcount, self.ancount, self.nscount, self.arcount])
        

class Question:
    # QNAME  : domain name represented by sequence of labels
    # QTYPE  : 16-bit code specifying type of query 
                # 0x0001 for type-A
                # 0x0002 for type-NS
                # 0x000f for type-MX
    # QCLASS : 16-bit code specifying class of query (should always be 0x0001, representing an Internet address)

    # Expected inputs: name (str), ty (str), class (int) 
    def __init__(self, name: str, ty: str, c=1):
        self.qName = encodeName(name)
        self.qType = encodeType(ty)
        self.qClass = c.to_bytes(2, 'big')

    def getSection(self):
        return b''.join([self.qName, self.qType, self.qClass])

def encodeName(name: str):
    lengths = getLengthsList(name)
    code = ''
    x = 0
    for i in range(0, len(lengths)):
        #code.append(lengths[i].to_bytes(2, 'big'))
        code += str(lengths[i])
        for j in range (0, lengths[i]):
            code += name[x]
            x += 1
        x += 1 # skip '.'
    code += '0' # 0 marks end of QNAME 
    #return code.encode('ascii')
    #z = [elem.encode('ascii') for elem in code]
    #return b''.join(z)
    return b'\x03\x77\x77\x77\x06\x6d\x63\x67\x69\x6c\x6c\x02\x63\x61\x00'

def getLengthsList(name: str):
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

def encodeType(ty: str) -> bytes:
    t = b'\x00\x00'
    if(ty.upper() == 'A'): t = b'\x00\x01'
    elif(ty.upper() == 'NS'): t = b'\x00\x02'
    elif(ty.upper() == 'MX'): t = b'\x00\x0f'
    return t

# x = encodeName('www.mcgill.ca')
# y = encodeType('mx')
# print(x)
# print(y)
# print(b''.join([x, y]))
# q = Question('www.google.com', 'NS', 1)
# print(q.getSection())
# p1 = Packet()
# h = Header()
# q = Question('www.mcgill.ca', 'A', 1)
# p1.addSection(h)
# p1.addSection(q)
# print(p1.pack)
# p2 = Packet(h, q)
# print(p2.pack)

    