from os import stat
import re
import sys
from socket import socket, AF_INET, SOCK_STREAM

from utils.all import logger, get_timestr_mil_sec, check_command
from states import trans_state 
from server_globals import break_condition, loop_condition
import server_globals as sg


check_command(num_args=2, correct_command="'python server.py <port>'")    

# server information
port = sys.argv[1]

# init server
socket_server = socket(AF_INET, SOCK_STREAM)
socket_server.bind(('', int(port)))

# server listening for connection
socket_server.listen(1)
logger(" PRIVATE | server is listening")

to_break = False
while True:
    sg.conn, addr = socket_server.accept()
    while True:
        command = sg.conn.recv(1024).decode()
        print(f"[{get_timestr_mil_sec()}]" + "< " + command)
        # service command
        ans = trans_state(command)
        if break_condition():
            to_break = True
        while loop_condition():        
            ans = trans_state()
        if to_break:
            to_break = False
            break
        
    
    