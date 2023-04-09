#S11 Group 5
# - Kimhoko, Jamuel Erwin 
# - Lim, Aurelius Justin
# - Mapua, Ramon Antonio

import socket
import json
import time
import threading

SERVER_HOST = "" #127.0.0.1
DESTINATION_PORT = 0 #12345

join_command = {"command": "join"}
leave_command = {"command": "leave"}
register_command = {"command": "register", "handle": "handle"}
all_message_command = {"command": "all", "message": "message"}
direct_message_command = {"command": "msg", "handle": "handle", "message": "message"}
error_command = {"command": "error", "message": "message"}

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.settimeout(1)

connected = False
registered = False

def receive():
    global connected, registered

    while True:
        try:
            data, server = clientSock.recvfrom(1024)
            data = data.decode("utf-8")
            json_data = json.loads(data)
        except:
            continue
        else:
            if json_data["command"] == "leave":
                print("Connection closed. Thank you!")
                connected = False
                registered = False
                runThread = False
            elif json_data["command"] == "register":
                print("Welcome, %s" %json_data["handle"])
                registered = True
            elif json_data["command"] == "all":
                print("%s" %json_data["message"])
            elif json_data["command"] == "msg":
                print("%s" %json_data["message"])
            else:
                print("%s" %json_data["message"])


def main(): 

    global connected, registered
    
    while True:

        while connected == False:
            user_input = input()

            if user_input == "":
                print("Please type a command.")
                continue

            processed_input = user_input.split()

            if  processed_input[0][0] != "/":
                print("Error: Command parameters do not match or is not allowed.")
                continue

            command = processed_input[0].lstrip("/")

            if command in ["leave", "register", "all", "msg"]:
                print("Error: Disconnection failed. Please connect to the server first.")
            elif command == "?":
                if len(processed_input) != 1:
                    print("Error: Command parameters do not match or is not allowed.")
                else:
                    print("COMMAND LIST:")
                    print("Connect to the server application: /join <server_ip_add> <port>\nDisconnect to the server application: /leave\nRegister a unique handle or alias: /register <handle>\nSend message to all: /all <message>\nSend direct message to a single handle: /msg <handle> <message>\nRequest command help to output all Input Syntax commands for references: /?")
                    
            elif command == "join":
                if len(processed_input) != 3:
                    print("Error: Command parameters do not match or is not allowed.")
                else:
                    is_ip = True
                    is_port = True
                    temp = processed_input[1].replace(".", "")
                    if temp.isnumeric() == False:
                        is_ip = False

                    ipbytes = processed_input[1].split(".")
                    if is_ip == True:
                        for ip_address_bytes in ipbytes:
                            if int(ip_address_bytes) < 0 or int(ip_address_bytes) > 255:
                                is_ip = False
                                break
                    is_port = processed_input[2].isnumeric()

                    if is_ip == False or is_port == False:
                        print("Error: Command parameters do not match or is not allowed.")
                    
                    else: 
                        SERVER_HOST = processed_input[1]
                        DESTINATION_PORT = int(processed_input[2])
                        clientSock.sendto(bytes(json.dumps(join_command), "utf-8"), (SERVER_HOST, DESTINATION_PORT))
                        try:
                            data, server = clientSock.recvfrom(1024)
                            data = data.decode("utf-8")
                            json_data = json.loads(data)
                        except:
                            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                        else:
                            if json_data["command"] == "error":
                                print(json_data["message"])
                            else:
                                print("Connection to the Message Board Server is successful!")
                                connected = True
            
            else:
                print("Error: Command not found")

        while connected == True:
            listener = threading.Thread(target=receive, args=( () ))
            listener.start()
            user_input = input()
            processed_input = user_input.split()

            if  processed_input[0][0] != "/":
                print("Error: Command parameters do not match or is not allowed.")
                continue

            command = processed_input[0].lstrip("/")

            if command == "join":
                print("You cannot do this command until you leave the current server.")
            
            elif command == "?":
                if len(processed_input) != 1:
                    print("Error: Command parameters do not match or is not allowed.")
                    continue
                print("COMMAND LIST:")
                print("Connect to the server application: /join <server_ip_add> <port>\nDisconnect to the server application: /leave\nRegister a unique handle or alias: /register <handle>\nSend message to all: /all <message>\nSend direct message to a single handle: /msg <handle> <message>\nRequest command help to output all Input Syntax commands for references: /?")
            
            elif command == "leave":
                if len(processed_input) != 1:
                    print("Error: Command parameters do not match or is not allowed.")
                    continue
                if registered == False:
                    print("Connection closed. Thank you!")
                    connected = False
                else:
                    clientSock.sendto(bytes(json.dumps(leave_command), "utf-8"), (SERVER_HOST, DESTINATION_PORT))
                    time.sleep(0.2)

            elif command == "register":
                if len(processed_input) != 2:
                    print("Error: Command parameters do not match or is not allowed.")
                    continue
                if registered == True:
                    print("Error: Cannot register because user is currently registered.")
                else:
                    register_command["handle"] = processed_input[1]
                    clientSock.sendto(bytes(json.dumps(register_command), "utf-8"), (SERVER_HOST, DESTINATION_PORT))
                    time.sleep(0.2)
            
            elif command == "all":
                if len(processed_input) == 1:
                    print("Error: Command parameters do not match or is not allowed.")
                    continue
                if registered == False:
                    print("You cannot message since you are not yet registered.")
                else:
                    i  = 1
                    final_message = ""
                    while i < len(processed_input):
                        if i == len(processed_input) - 1:
                            final_message += processed_input[i]
                        else:
                            final_message += processed_input[i] + " "
                        
                        i += 1
                    all_message_command["message"] = final_message
                    clientSock.sendto(bytes(json.dumps(all_message_command), "utf-8"), (SERVER_HOST, DESTINATION_PORT))

            elif command == "msg":
                if len(processed_input) == 1 or len(processed_input) == 2:
                    print("Error: Command parameters do not match or is not allowed.")
                    continue
                if registered == False:
                    print("Error: Cannot message as user is not yet registered.")
                else:
                    i  = 2
                    final_message = ""
                    while i < len(processed_input):
                        if i == len(processed_input) - 1:
                            final_message += processed_input[i]
                        else:
                            final_message += processed_input[i] + " "
                        i += 1
                    direct_message_command["handle"] = processed_input[1]
                    direct_message_command["message"] = final_message
                    clientSock.sendto(bytes(json.dumps(direct_message_command), "utf-8"), (SERVER_HOST, DESTINATION_PORT))
                    time.sleep(0.2)

            else:
                clientSock.sendto(bytes(json.dumps({"command":command}), "utf-8"), (SERVER_HOST, DESTINATION_PORT))
                time.sleep(0.2)
        clientSock.close
    
if __name__ == '__main__':
    main()
