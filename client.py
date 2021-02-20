import argparse
import time
from sys import argv
import socket

# Use the argparse package to parse the aruments for files and ts/rs server ports
parser = argparse.ArgumentParser()

parser.add_argument('-f', type=str, default='PROJI-HNS.txt', action='store', dest='in_file')
parser.add_argument('-o', type=str, default='RESOLVED.txt',
                    action='store', dest='out_file')

parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',
                    action='store')
parser.add_argument('rsListenPort', type=int, help='This is the port to connect to the server on rsListenPort',
                    action='store')
parser.add_argument('tsListenPort', type=int, help='This is the port to connect to the server on tsListenPort',
                    action='store')
args = parser.parse_args(argv[1:])


# create a client sock for rs server
rsclient_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rsserver_addr = (args.server_location, args.rsListenPort)
rsclient_sock.connect(rsserver_addr)

#create a client sock for ts server
tsclient_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tsserver_addr = (args.server_location, args.tsListenPort)
tsclient_sock.connect(tsserver_addr)


#write to out_file w for each line read in in_file r
with open(args.out_file, 'w') as write_file:
    for line in open(args.in_file, 'r'):

        #trim the line to avoid weird new line things
        line = line.strip()

        #Check if the rs server contains the line's domain name or ip
        if line:
            rsclient_sock.sendall(line.encode('utf-8'))
            answer = rsclient_sock.recv(256)
            answer = answer.decode('utf-8')
            
        #Check the answer given from rs server. If it contains "NS" then ask ts server
        if "NS" in answer:
            #checking ts server for the line's domain name or ip
            tsclient_sock.sendall(line.encode('utf-8'))
            tsanswer = tsclient_sock.recv(256).decode('utf-8')
            #write the ts server's answer. This will either be "A" or "Error:HOST NOT FOUND"
            write_file.write(line + tsanswer + '\n')
            continue

        #if the answer from rs server was not "NS" then we want to write that
        else:
            write_file.write(line + answer + '\n')

# close the socket (note this will be visible to the other side)
tsclient_sock.close()
rsclient_sock.close()
