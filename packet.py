# Putting together request packets

import random

# Note: This class only contains Header and Question attributes
#         because it is only used from request packets
class Packet:
    def __init__(self, header=None, question=None):
        self.pack = b''
        if(header != None): 
            self.pack = b''.join([self.pack, header.getSection()])
            if(question != None):
                self.pack = b''.join([self.pack, question.getSection()])

    
    ## Expectation: Sections are added in order ##
    # ASSUMPTION: Arg 'c' has a method called getSection()
    #               which returns the entire section as a bytes object
    def addSection(self, c):
        self.pack = b''.join([self.pack, c.getSection()])
        return self.pack

# All attributes are in bytes
class Header:
    ## NOTE: Information about the values for these attributes comes from the dnsprimer.pdf document provided
    # ID      : 16-bit              ; should be random
    # QR      : 1-bit               ; query (0) or response (1)
    # Opcode  : 4-bit               ; should be 0, representing standard query
    # AA      : 1-bit               ; for responses, whether (1) or not (0) the name server is an authority 
    # TC      : 1-bit               ; whether (1) or not (0) message was truncated
    # RD      : 1-bit               ; set to 1 to indicate we desire recursion
    # RA      : 1-bit               
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
        id = random.getrandbits(16)     # returns a non-negative integer with k random bits
        self.id = id.to_bytes(2, 'big')
        self.flags = b'\x01\x00'
        self.qdcount = b'\x00\x01'
        self.ancount = b'\x00\x00'
        self.nscount = b'\x00\x00'
        self.arcount = b'\x00\x00'

    # This function joins all the attributes of this class into a single bytes object
    #   and returns it
    def getSection(self):
        return b''.join([self.id, self.flags, self.qdcount, self.ancount, self.nscount, self.arcount])
        
# All attributes are in bytes
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

    # This function joins all the attributes of this class into a single bytes object
    #   and returns it
    def getSection(self):
        return b''.join([self.qName, self.qType, self.qClass])

# Input:  domain name (string)
# Output: name encoded in a bytes object ending with a 0, 
#           representing all the labels in the name prefixed by their length
def encodeName(name: str):
    lengths = getLengthsList(name)
    code = b''  # final encoding 
    x = 0       # iterate through 'name'
    for i in range(0, len(lengths)): # for each label
        code += lengths[i].to_bytes(1, 'big') # prefix label with its length (in bytes)
        codeStr = ''    # encode label 
        for j in range (0, lengths[i]): # label length
            codeStr += name[x]
            x += 1
        x += 1 # skip '.'
        code += codeStr.encode() # add label encoding to final encoding
    code += b'\x00' # 0 marks end of QNAME 
    return code

def getLengthsList(name: str):
    lengths = []
    count = 0
    for i in range(0, len(name)):   # iterate though each character in 'name'
        if(name[i] == '.'):         # stop when (another) '.' reached
            lengths.append(count)   # add length number to list
            count = 0               # reset count
        else:
            count += 1
    lastI = 0
    for i in range(0, len(lengths)): lastI += (lengths[i] + 1)  # get index of last label
    lastLength = len(name) - lastI    # calcualte length of last label
    lengths.append(lastLength)
    return lengths

# Input:  type (string)
# Output: byte object (length 2) representing type in ASCII
# Note: input validation for given query types is done before this method is called
def encodeType(ty: str) -> bytes:
    t = b'\x00\x00'
    if(ty.upper() == 'A'): t = b'\x00\x01'
    elif(ty.upper() == 'NS'): t = b'\x00\x02'
    elif(ty.upper() == 'MX'): t = b'\x00\x0f'
    return t
