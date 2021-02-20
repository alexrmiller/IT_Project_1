# server
import socket
import sys
import argparse
from sys import argv
import binascii
import struct

parser = argparse.ArgumentParser(description="""rs Port""")
parser.add_argument('rsListenPort', type=int, action='store')
parser.add_argument('-f', type=str, default='PROJI-DNSRS.txt', action='store', dest='in_file')
args = parser.parse_args(argv[1:])


# form key values for in_file using Hashmap
table = {}
with open('PROJI-DNSRS.txt', 'r') as file:
    for line in file:
        host, ipAddress, flag = line.strip().split(' ')
        table[host] = ipAddress, flag

# use socket() function to start socket protocal
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # FOR LOCAL CLIENT HANDLING

# bind the rs.py to client.py
serverSock.bind(('', args.rsListenPort))

# after binding, listen to client
serverSock.listen(1)
newSock, serverAddress = serverSock.accept()

# while the server is listening it checks then decodes messages
with newSock:
    while True:
        txtReceived = newSock.recv(512)
        txt = txtReceived.decode('utf-8').lower()
        if not txtReceived:
            break
        if txt in table:
            #if there is a match then send that match back
            text = table.get(txt)
            print(text)
            untuplemessage = " "+ text[0] +" " + text[1]
            newSock.send(untuplemessage.encode('utf-8'))
            socket.setdefaulttimeout(10)
        else:
            # If there is no match, RS sends the string
            text = table.get('localhost')
            untuplemessage = " " + text[0] + " " + text[1]
            newSock.send(untuplemessage.encode('utf-8'))
            #newSock.close()
            socket.setdefaulttimeout(10)
            
# close socket
newSock.close()
exit()
