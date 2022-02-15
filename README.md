# ECSE316
# Assignment 1: Network Programming and DNS

## Names and McGill IDs
* Amani Jammoul 260381641

* Ramin Akhavan-Sarraf 260904764

## How to run our program
Run the main dnsClient.py file as such:

&nbsp;&nbsp; **python3 dnsClient.py [-t timeout] [-r max-retries] [-p port] [-mx|ns] server name**

## Note
Our program expects that the server IPv4 address (2nd to last input) is given as-is, *without* a prefixing '@' symbol. It will not work with the '@' at the front of the server address. If you run it with the '@', our program should print a message saying not to do so. (The reason for this is that when running the program on Windows terminal, anything with an '@' at the front is not recognized as an argument).

## Files in our submission
* ECSE316_Assignment1_Report.pdf (Report)

### In a zip file
* dnsClient.py (main file)

* queries.py

* reponse.py

* packet.py

* packet_decoding.py
