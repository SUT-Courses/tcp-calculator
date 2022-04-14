from os import stat
import re
import sys
from socket import socket, AF_INET, SOCK_STREAM

from utils.all import logger, get_timestr_mil_sec, input_, check_command, error_message, is_Z_number

check_command(num_args=2, correct_command="'python server.py <port>'")    

# server information
port = sys.argv[1]
# port = 5000
conn = None
socket_server = socket(AF_INET, SOCK_STREAM)
socket_server.bind(('', int(port)))

socket_server.listen(1)
logger(" PRIVATE | server is listening")

states = {
    -1: {"state_name": "error", "candidate_next": ["begin"], "need_input": False},
    0: {"state_name": "begin", "candidate_next": ["error", "<number_1>", "exit", "help"], "need_input": True, "inputs": ["start", "clear", "exit", "help"]},
    1: {"state_name": "<number_1>", "candidate_next": ["error", "exit", "<number_2>", "clear", "help"], "need_input": True, "inputs": ["exit", "clear", "<number>", "help"]},
    2: {"state_name": "exit", "candidate_next": [], "need_input": False},
    3: {"state_name": "<number_2>", "candidate_next": ["error", "exit", "<operator>", "clear", "help"], "need_input": True, "inputs": ["exit", "clear", "<number>", "help"]},
    4: {"state_name": "<operator>", "candidate_next": ["error", "exit", "result", "clear", "help"], "need_input": True, "inputs": ["exit", "clear", "<operator>", "help"]},
    5: {"state_name": "result", "candidate_next": ["error", "begin"], "need_input": False},
    6: {"state_name": "clear", "candidate_next": ["begin"], "need_input": False},
}

current_state:dict = None
output:int = None
equation:str = ""
ans = None



def out(msg: str, error=False):
    conn.send(f"{msg}".encode())
    if error:
        error_message(" RESPONSE | " + msg)
    else:
        logger(" RESPONSE | " + msg)

def _set_state_id(name: str):
    global current_state
    for stateid in states:
        if states[stateid]["state_name"] == name:
            current_state = states[stateid]
            logger(f" PRIVATE | server new state: {name}")
            return None
    raise ValueError(f"State {name} not found")

def trans_state(command=""):
    global equation, output
    current_state_name = current_state["state_name"]
    if command == "help":
        out(f"Your state is {current_state_name} and you can input the following ... {current_state['inputs']}")
    elif current_state_name == "error":
        equation = ""
        _set_state_id("begin")
    elif current_state_name == "begin":
        if command == "exit":
            _set_state_id("exit")
        elif command == "start":
            _set_state_id("<number_1>")
            out("OK")
        elif command == "clear":
            _set_state_id("begin")
            out("cleared")
        else: 
            out(f"Not valid input", error = True)
            _set_state_id("error")
    
    elif current_state_name == "<number_1>":
        if command == "exit":
            _set_state_id("exit")
        elif is_Z_number(command):
            equation += command
            out("ghost")
            _set_state_id("<number_2>")
        elif command == "clear":
            _set_state_id("begin")
            out("cleared")
        else:
            out(f"Not valid input", error=True)
            _set_state_id("error")
    elif current_state_name == "exit":
        out("exit done")
        conn.close()
        _set_state_id("begin")
        return None
        
    elif current_state_name == "<number_2>":
        if command == "exit":
            _set_state_id("exit")
        elif is_Z_number(command):
            equation += ' ' + command
            out("ghost")
            _set_state_id("<operator>")
        elif command == "clear":
            _set_state_id("begin")
            out("cleared")
        else:
            out(f"Not valid input", error=True)
            _set_state_id("error")
    elif current_state_name == "<operator>":
        if command == "exit":
            _set_state_id("exit")
        elif command == "clear":
            _set_state_id("begin")
            out("cleared")
        elif command in ["+", "-", "*", "/"]:
            equation = equation.replace(" ", command)
            _set_state_id("result")

        else: 
            out(f"Not valid input", error=True)
            _set_state_id("error")
        
    elif current_state_name == "result":
        try:
            output = eval(equation)
            out(str(output))
            equation = ""
            _set_state_id("begin")
            return output
        except Exception as e:
            output = None
            out(f"{e}", error=True)
            _set_state_id("error")
    else:
        raise ValueError(f"State {current_state_name} not found")  
    
        
_set_state_id("begin")
to_break = False
while True:
    conn, addr = socket_server.accept()
    while True:
        command = conn.recv(1024).decode()
        print(f"[{get_timestr_mil_sec()}]" + "> " + command)
        trans_state(command)
        if current_state["state_name"] == "exit":
            to_break = True
        while not current_state["need_input"]:        
            ans = trans_state()
        if to_break:
            to_break = False
            break
        
    
    