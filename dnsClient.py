import sys
from queries import *

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
print(query.send())



