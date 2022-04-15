from socket import socket, AF_INET, SOCK_STREAM

from utils.all import logger, get_timestr_mil_sec, input_, check_command, error_message, is_Z_number
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
        out(f"Your state is {current_state_name} and you can input the following ... {sg.current_state['inputs']}")
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
        close_connection()
        _set_state_id("begin")
        return 
        
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
    
def break_condition():
    if sg.current_state["state_name"] == "exit":
        return True
    return False
    

def loop_condition():
    return not sg.current_state["need_input"]    

_set_state_id("begin")