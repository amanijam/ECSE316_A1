# Putting together the packets, which are made up of the Header and the Question (2 classes?)

class Packet:
    # Header, Question, Answer, Authority, Additional
    def __init__(self, header, question, answer=None, auth=None, add=None):
        self.header = header
        self.question = question


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
    def __init__(self, qr):
        self.qr = qr
        


class Question:
    # QNAME  : domain name represented by sequence of labels
    # QTYPE  : 16-bit code specifying type of query 
                # 0x0001 for type-A
                # 0x0002 for type-NS
                # 0x000f for type-MX
    # QCLASS : 16-bit code specifying class of query (should always be 0x0001, representing an Internet address)
    def __init__(self, qName, qType):
        self.qName = qName
        self.qType = qType

    