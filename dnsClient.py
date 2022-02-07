import sys

# Default values
timeout, maxr, port, mx, nx = 5, 3, 53, False, False
server, name = None, None

# Parse input with expected format: python dnsClient [-t timeout] [-r max-retries] [-p port] [-mx|ns] @server name
if len(sys.argv) < 3: print("ERROR: Not enough arguments")
else:
    i = 1
    while(i < len(sys.argv)-2):
        if(sys.argv[i] == '-t'):
            timeout = sys.argv[i + 1]
            i += 2
            continue
        elif(sys.argv[i] == '-r'):
            maxr = sys.argv[i + 1]
            i += 2
            continue
        elif(sys.argv[i] == '-p'):
            port = sys.argv[i + 1]
            i += 2
            continue
        elif(sys.argv[i] == '-mx'): 
            mx = True
            i += 1
            continue
        elif(sys.argv[i] == '-nx'):
            nx = True
            i += 1
            continue
        else:
            print("Error: Unknown arg")
            break
    server = sys.argv[-2]
    name = sys.argv[-1]
    print('{} {} {} {} {} {} {}'.format(timeout, maxr, port, mx, nx, server, name))

