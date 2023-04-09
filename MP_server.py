#S11 Group 5
# - Kimhoko, Jamuel Erwin 
# - Lim, Aurelius Justin
# - Mapua, Ramon Antonio

import socket
import json

UDP_IP_ADDRESS = input("Enter listening address: ") #127.0.0.1
UDP_PORT_NO = input("Enter listening port number: ") #12345
UDP_PORT_NO = int(UDP_PORT_NO)

handles = []
connections = []

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Server starting on %s port %d" %(UDP_IP_ADDRESS, UDP_PORT_NO))
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

print("\nServer established on %s port %d." %(UDP_IP_ADDRESS, UDP_PORT_NO))

while True:
    print("\nWaiting to receive messages...")

    data, address = serverSock.recvfrom(1024)
    data = data.decode("utf-8")
    json_data = json.loads(data)
    print("\nReceived message: ", data, "\n from ", address)

    # Connect
    if json_data["command"] == "join":
        if address[0] != UDP_IP_ADDRESS or address[1] == UDP_PORT_NO:
            command = bytes(json.dumps({"command":"error", "message":"Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number."}), "utf-8")
            print("Unable to connect due to incorrect IP Address and Port.")
            serverSock.sendto(command, address)
        else:
            command = bytes(json.dumps({"command": "join"}), "utf-8")
            serverSock.sendto(command, address)

    # Leave
    elif json_data["command"] == "leave":
        connection_index = connections.index(address)
        deleted_user = handles.pop(connection_index)
        deleted_connection = connections.pop(connection_index)
        print("User %s have left the message board." %deleted_user)
        command = bytes(json.dumps({"command": "leave"}), "utf-8")
        serverSock.sendto(command, address)

    # Registration
    elif json_data["command"] == "register":
        if json_data["handle"] in handles:
            command = bytes(json.dumps({"command":"error", "message":"Error: Registration failed. Handle or alias already exists."}), "utf-8")
            print("Handle %s is already in use." %json_data["handle"])
            serverSock.sendto(command, address)
        else:
            handles.append(json_data["handle"])
            connections.append(address)
            command = bytes(json.dumps({"command": "register", "handle": handles[len(handles) - 1]}), "utf-8")
            serverSock.sendto(command, address)

    # Send message to all
    elif json_data["command"] == "all":
        sender_index = connections.index(address)
        sender = handles[sender_index]
        message = sender + ": " + json_data["message"]
        print(message)

        command = bytes(json.dumps({"command": "all", "message": message}), "utf-8")

        i = 0

        while i < len(connections):
            serverSock.sendto(command, connections[i])
            i += 1
            
    # Direct message
    elif json_data["command"] == "msg":
        if json_data["handle"] not in handles:
            command = bytes(json.dumps({"command":"error", "message":"Error: Handle or alias not found."}), "utf-8")
            print("Handle %s is not registered.", json_data["handle"])
            serverSock.sendto(command, address)
        else:
            sender_index = connections.index(address)
            sender = handles[sender_index]
            recipient_message = "[From %s]: %s" %(sender, json_data["message"])
            
            
            recepient_index = handles.index(json_data["handle"])
            recipient_address = connections[recepient_index]
            sender_message = "[To %s]: %s" %(json_data["handle"], json_data["message"])

            command = bytes(json.dumps({"command": "msg", "handle": sender ,"message": recipient_message}), "utf-8")
            serverSock.sendto(command, recipient_address)
            command = bytes(json.dumps({"command": "msg", "handle": json_data["handle"] ,"message": sender_message}), "utf-8")
            serverSock.sendto(command, address)
    
    #Incorrect parameters
    elif ((json_data["command"] == "register" and json_data["handle"] == None) or (json_data["command"] == "all" and json_data["message"] == None) or (json_data["command"] == "msg" and (json_data["handle"] == None or json_data["message"] == None))):
        command = bytes(json.dumps({"command":"error", "message":"Error: Command parameters do not match or is not allowed."}), "utf-8")
        print("Incorrect or invalid command parameters")
        serverSock.sendto(command, address)
    
    else:
        command = bytes(json.dumps({"command":"error", "message":"Error: Command not found"}), "utf-8")
        print("Command not found")
        serverSock.sendto(command, address)
        
    serverSock.close
