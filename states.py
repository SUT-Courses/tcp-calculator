from os import stat
import re
import sys
from utils.all import error_message, logger


states = {
    -1: {"state_name": "error", "candidate_next": ["begin"], "need_input": False},
    0: {"state_name": "begin", "candidate_next": ["error", "number_1", "exit"], "need_input": True},
    1: {"state_name": "number_1", "candidate_next": ["error", "exit", "number_2"], "need_input": True},
    2: {"state_name": "exit", "candidate_next": [], "need_input": False},
    3: {"state_name": "number_2", "candidate_next": ["error", "exit", "operator"], "need_input": True},
    4: {"state_name": "operator", "candidate_next": ["error", "exit", "result"], "need_input": True},
    5: {"state_name": "result", "candidate_next": ["error", "begin"], "need_input": False},
}

current_state:dict = None
output:int = None
equation:str = ""
ans = None
def _set_state_id(name: str):
    global current_state
    for stateid in states:
        if states[stateid]["state_name"] == name:
            current_state = states[stateid]
            logger(f"new state = {name}")
            return None
    raise ValueError(f"State {name} not found")

def trans_state(command=""):
    global equation, output
    current_state_name = current_state["state_name"]
    if current_state_name == "error":
        equation = ""
        _set_state_id("begin")
    elif current_state_name == "begin":
        if command == "exit":
            _set_state_id("exit")
        elif command == "start":
            _set_state_id("number_1")
        else: 
            error_message(f"Not valid input")
            _set_state_id("error")
    
    elif current_state_name == "number_1":
        if command == "exit":
            _set_state_id("exit")
        elif command.isdigit():
            equation += command
            _set_state_id("number_2")
        else:
            error_message(f"Not valid input")
            _set_state_id("error")
    elif current_state_name == "exit":
        sys.exit()
    elif current_state_name == "number_2":
        if command == "exit":
            _set_state_id("exit")
        elif command.isdigit():
            equation += ' ' + command
            _set_state_id("operator")
        else:
            error_message(f"Not valid input")
            _set_state_id("error")
    elif current_state_name == "operator":
        if command == "exit":
            _set_state_id("exit")
        elif command in ["+", "-", "*", "/"]:
            equation = equation.replace(" ", command)
            _set_state_id("result")

        else: 
            error_message(f"Not valid input")
            _set_state_id("error")
        
    elif current_state_name == "result":
        try:
            output = eval(equation)
            equation = ""
            _set_state_id("begin")
            return output
        except Exception as e:
            output = None
            error_message(f"{e}")
            _set_state_id("error")
    else:
        raise ValueError(f"State {current_state_name} not found")  
    
        
_set_state_id("begin")

while True:
    command = input()
    trans_state(command)
    while not current_state["need_input"]:        
        ans = trans_state()
    if ans and ans is not None:
        print(ans)
    
        
    
    