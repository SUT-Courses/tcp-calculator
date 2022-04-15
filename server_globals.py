from utils.all import error_message, logger

conn = None

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

def out(msg: str, error=False):
    conn.send(f"{msg}".encode())
    if error:
        error_message(" RESPONSE | " + msg)
    else:
        logger(" RESPONSE | " + msg)
        
def close_connection():
    conn.close()
    logger(" PRIVATE | server connection closed")