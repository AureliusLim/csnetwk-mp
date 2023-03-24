import json
import socket
import threading
import time

server_IP = ""
PORT_NO = 0

join_command = {"command": "join"}
leave_command = {"command": "leave"}
register_command = {"command": "register", "handle": "handle"}
all_message_command = {"command": "all", "message": "message"}
direct_message_command = {"command": "msg", "handle": "handle", "message": "message"}
error_command = {"command": "error", "message": "message"}


client_socket= socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
client_socket.settimeout(1)

