import socket
import json

IP_ADDRESS = input("Enter address to listen: ")
PORT_NO = int(input("Enter port number: "))
bufferSize = 1024

#create datagram socket
server_socket= socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

#bind to address and ip
server_socket.bind((IP_ADDRESS, PORT_NO))

#continue listening

while(True):
    byte_address = server_socket.recvfrom(bufferSize)
    received_data = byte_address[0]
    received_json = json.loads(received_data.decode("utf-8"))
