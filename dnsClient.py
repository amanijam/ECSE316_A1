from imaplib import Time2Internaldate
import sys
import timeit
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
# 10: (unexpected response) Incorrect answer class
# 11: Max retries exceeded
 
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
        elif(sys.argv[i] == '-ns'):
            rType = 'NS'
            i += 1
            continue
        else:
            print("ERROR Expected Syntax: {}".format(expSyntax))
            break
# if(sys.argv[-2])[0] == '@': server = sys.argv[-2][1:]
# else: sys.exit("ERROR Expected Syntax: {}".format(expSyntax))
server = sys.argv[-2][1:]
name = sys.argv[-1]

print("\nDNS Client sending request for {}".format(name))
print("Server: {}".format(server))
print("Request type: {}".format(rType))

query = Query(server, name, timeout, maxR, port, rType)
start_time = timeit.timeit()
return_val, response = query.send()
retries = 0
while(retries < maxR):
    if(return_val == 6): # resend
        return_val = query.send()
        retries += 1
    else:
        break #SUCCESS

if retries == maxR:
    return_val = 11
end_time = timeit.timeit()
response_time = end_time - start_time
print("\nResponse received after " + str(response_time) + " seconds (" + str(retries) + " retries)")
## TODO: Add descriptions to these errors ##
if(return_val == 1):
    print("\nERROR\tFormat error: name server was unable to interpret the query")
elif(return_val == 2): 
    print("\nERROR\tServer failure: name server was unable to process this query due to a problem with the name server")
elif(return_val == 3):
    print("\nERROR\tName error: domain name specified in query does not exist")
elif(return_val == 4): 
    print("\nERROR\tNot implemented: name server does not support the requested kind of query")
elif(return_val == 5): 
    print("\nERROR\tRefused: the name server refuses to perform the requested operation for policy reasons")
elif(return_val == 6): 
    print("\nERROR\tTimeout Error: the time exceeded the timeout value of " + str(query.timeout) + " seconds")
elif(return_val == 7): 
    print("\nNOTFOUND\t no record found")
elif (return_val == 8):
    print("\nERROR\tUnexpected response: response ID does not match Request ID")
elif (return_val == 9):
    print("\nERROR\tUnexpected response: response packet indicates that it is a request (QR = 0) ")
elif (return_val == 10):
    print("\nERROR\tUnexpected response: class in Answer section of the response packet is not set to 1")
elif(return_val == 11): 
    print("\nERROR\tMax retries of " + query.maxR + " exceeded")
else:
    response.display_response()
# decoder = Packet_Decoder(data, query.header.id)
# decoder.decode_packet()



