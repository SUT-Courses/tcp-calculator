from socket import socket, AF_INET, SOCK_STREAM

from utils.all import logger, is_Z_number
from server_globals import out, close_connection, states
import server_globals as sg


output:int = None
equation:str = ""


# change state using its name
def _set_state_id(name: str):
    for stateid in states:
        if states[stateid]["state_name"] == name:
            sg.current_state = states[stateid]
            logger(f" PRIVATE | server new state: {name}")
            return None
    raise ValueError(f"State {name} not found")

# go to next state based on input commands
def trans_state(command=""):
    global equation, output
    current_state_name = sg.current_state["state_name"]
    if command == "help":
        # send to client current_state and options of input
        out(f"Your state is {current_state_name} and you can input the following ... {sg.current_state['inputs']}")
    elif current_state_name == "error":
        # handle errors here
        equation = ""
        _set_state_id("begin")
    elif current_state_name == "begin":
        # init state
        if command == "exit":
            _set_state_id("exit")
        elif command == "start":
            start_actions()
        elif command == "clear":
            refresh_state()
        else: 
            not_valid_input_error()
    
    elif current_state_name == "<number_1>":
        if command == "exit":
            _set_state_id("exit")
        # number1 sent from client
        elif is_Z_number(command):
            equation += command
            out("ghost")
            _set_state_id("<number_2>")
        elif command == "clear":
            refresh_state()
        else:
            not_valid_input_error()
            
    elif current_state_name == "exit":
        out("exit done")
        close_connection()
        _set_state_id("begin")
        return 
        
    elif current_state_name == "<number_2>":
        if command == "exit":
            _set_state_id("exit")
        # number2 sent from client
        elif is_Z_number(command):
            equation += ' ' + command
            out("ghost")
            _set_state_id("<operator>")
        elif command == "clear":
            refresh_state()
        else:
            not_valid_input_error()
            
    elif current_state_name == "<operator>":
        if command == "exit":
            _set_state_id("exit")
        elif command == "clear":
            refresh_state()
        # operator sent from client
        elif command in ["+", "-", "*", "/"]:
            equation = equation.replace(" ", command)
            _set_state_id("result")

        else: 
            not_valid_input_error()
        
    elif current_state_name == "result":
        try:
            # calculation is here
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

# start actions
def start_actions():
    _set_state_id("<number_1>")
    out("OK")

# clear command actions
def refresh_state():
    _set_state_id("begin")
    out("cleared")

# send error message to client
def not_valid_input_error():
    out(f"Not valid input", error = True)
    _set_state_id("error") 
       
# init state
_set_state_id("begin")