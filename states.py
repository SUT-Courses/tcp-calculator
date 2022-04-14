from os import stat
import re
import sys
from utils.all import error_message, logger, is_Z_number


states = {
    -1: {"state_name": "error", "candidate_next": ["begin"], "need_input": False},
    0: {"state_name": "begin", "candidate_next": ["error", "<number_1>", "exit"], "need_input": True},
    1: {"state_name": "<number_1>", "candidate_next": ["error", "exit", "<number_2>", "clear"], "need_input": True},
    2: {"state_name": "exit", "candidate_next": [], "need_input": False},
    3: {"state_name": "<number_2>", "candidate_next": ["error", "exit", "<operator>", "clear"], "need_input": True},
    4: {"state_name": "<operator>", "candidate_next": ["error", "exit", "result", "clear"], "need_input": True},
    5: {"state_name": "result", "candidate_next": ["error", "begin"], "need_input": False},
    6: {"state_name": "clear", "candidate_next": ["begin"], "need_input": False},
}

current_state:dict = None
output:int = None
equation:str = ""
ans = None
outputs = []



def out(msg: str, error=False):
    outputs.append(output)
    if error:
        error_message(msg)
    else:
        logger(msg)

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
        out(f"You can input the following ...\n\t\t\t\t{[x for x in current_state['candidate_next'] if x != 'error']}")
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
            _set_state_id("<number_2>")
        elif command == "clear":
            _set_state_id("begin")
            out("cleared")
        else:
            out(f"Not valid input", error=True)
            _set_state_id("error")
    elif current_state_name == "exit":
        sys.exit() # end connection
    elif current_state_name == "<number_2>":
        if command == "exit":
            _set_state_id("exit")
        elif is_Z_number(command):
            equation += ' ' + command
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
            out(output)
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

while True:
    command = input()
    trans_state(command)
    while not current_state["need_input"]:        
        ans = trans_state()
    
        
    
    