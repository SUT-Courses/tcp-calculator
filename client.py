# sajad faghfoor maghrebi
# 97106187

import sys
import time
from socket import AF_INET, socket, SOCK_STREAM, timeout

from utils.all import logger, get_timestr_mil_sec, input_, check_command

check_command(num_args=2, correct_command="'python client.py <port>'")    

# server information
host, port = "127.0.0.1", sys.argv[1]
socket_client = socket(AF_INET, SOCK_STREAM)
socket_client.connect((host, int(port)))
while True:
    command = input(f"\t\t\t " + "> ")
    if not command.strip():
        continue
    socket_client.send(command.encode())
    log = socket_client.recv(1024).decode()
    if log != "ghost":
        logger(log)
    if log == "exit done":
        break
    