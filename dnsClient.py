import sys
from queries import *

# Default values
timeout, maxR, port, rType = 5, 3, 53, 'A'
server, name = None, None

expSyntax = "dnsClient.py [-t timeout] [-r max-retries] [-p port] [-mx|ns] server name"

# Parse input with expected format: python dnsClient.py [-t timeout] [-r max-retries] [-p port] [-mx|ns] @server name
if len(sys.argv) < 3: 
    print("ERROR\tNot enough args\n\tExpected Syntax: {}".format(expSyntax))
elif len(sys.argv) > 6: 
    print("ERROR\tToo many args\n\tExpected Syntax: {}".format(expSyntax))
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
            print("ERROR\t\"{}\" is not recognized as an arg\n\tExpected Syntax: {}".format(sys.argv[i], expSyntax))
            exit(1)
    

    if(sys.argv[-2][0] == '@'): 
        print("ERROR\tServer address should not be prefixed with \"@\"\n\tExpected Syntax: {}".format(expSyntax))
        exit(1)
    else: server = sys.argv[-2]
    name = sys.argv[-1]
    
    print("DNS Client sending request for {}".format(name))
    print("Server: {}".format(server))
    print("Request type: {}".format(rType))

    query = Query(server, name, timeout, maxR, port, rType)
    query.send()



