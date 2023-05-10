# ECSE316
# Assignment 1: Network Programming and DNS

## Group number, Names and McGill IDs
* Group 14

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

## Assignemnt Description
![A1 - 1 of 4](https://github.com/amanijam/ECSE316_A1/assets/19826681/93cd3af6-96a0-41cb-9931-b5ecae8f58f4)
![A1 - 2 of 4](https://github.com/amanijam/ECSE316_A1/assets/19826681/45aff3d3-97c9-409c-bbd5-e56fbca0f914)
![A1 - 3 of 4](https://github.com/amanijam/ECSE316_A1/assets/19826681/d4bb6768-c252-4b81-9a3c-9a2211a49011)
![A1 - 4 of 4](https://github.com/amanijam/ECSE316_A1/assets/19826681/2f98caa2-fb31-4602-928d-e7076d6eddfa)


