from imaplib import Time2Internaldate
import sys
import time
from urllib import response
from queries import *
from packet_decoding import *

# Error codes:
# 0 : success
# 1 : Format error: name server was unable to interpret the query
# 2 : Server failure: name server was unable to process this query due to a problem with the name server
# 3 : Name error: meaningful only for responses from an authoritative name server, this code
        # signifies that the domain name referenced in the query does not exist
# 4 : Not implemented: name server does not support the requested kind of query
# 5 : Refused: the name server refuses to perform the requested operation for policy reasons
# 6 : Timeout Error
# 7 : No response (nothing in Answer or Additional section)
# 8 : (unexpected response) Response ID does not match Request ID
# 9 : (unexpected response) Code indicates a request (0) 

# Default values
timeout, maxR, port, rType = 5, 3, 53, 'A'
server, name = None, None

expSyntax = "dnsClient [-t timeout] [-r max-retries] [-p port] [-mx|ns] @server name"

# Parse input with expected format: python dnsClient [-t timeout] [-r max-retries] [-p port] [-mx|ns] @server name
if len(sys.argv) < 3: print("Not enough args")
else:
    i = 1
    while(i < len(sys.argv)-2):
        if(sys.argv[i] == '-t'):
            timeout = sys.argv[i + 1]
            i += 2
            continue
        elif(sys.argv[i] == '-r'):
            maxR = sys.argv[i + 1]
            i += 2
            continue
        elif(sys.argv[i] == '-p'):
            port = sys.argv[i + 1]
            i += 2
            continue
        elif(sys.argv[i] == '-mx'): 
            rType = 'MX'
            i += 1
            continue
        elif(sys.argv[i] == '-nx'):
            rType = 'NX'
            i += 1
            continue
        else:
            print("ERROR Expected Syntax: {}".format(expSyntax))
            break
# if(sys.argv[-2])[0] == '@': server = sys.argv[-2][1:]
# else: sys.exit("ERROR Expected Syntax: {}".format(expSyntax))
server = sys.argv[-2]
name = sys.argv[-1]

print("DNS Client sending request for {}".format(name))
print("Server: {}".format(server))
print("Request type: {}".format(rType))

query = Query(server, name, timeout, maxR, port, rType)
response = query.send()
tries = 1
while(tries < maxR):
    if(response == 1 or
       response == 2 or
       response == 3 or
       response == 4 or
       response == 5 or
       response == 7): 
        break
    elif(response == 6): # resend
        response = query.send()
        tries += 1
    else:
        print(response)
        break #SUCCESS

## TODO: Add descriptions to these errors ##
if(response == 1):
    print("ERROR\t")
elif(response == 2): 
    print("ERROR\t")
elif(response == 3):
    print("ERROR\t")
elif(response == 4): 
    print("ERROR\t")
elif(response == 5): 
    print("ERROR\t")
elif(response == 6): 
    print("ERROR\t")
elif(response == 7): 
    print("NOTFOUND")
# decoder = Packet_Decoder(data, query.header.id)
# decoder.decode_packet()



