from datetime import datetime
import sys



def logger(msg: str):
    # print time and message
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}] {msg}')

def error_message(msg: str):
    # print error message
    logger(msg=f"🔥{msg}🔥")

def is_Z_number(msg):
    if msg.isdigit():
        return True
    if msg and msg[0] == '-' and msg[1:].isdigit():
        return True
    return False
    
def get_timestr_mil_sec() -> str:
    # get milliseconds from datetime 
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
def check_command(num_args, correct_command, exit_code=1):
    if len(sys.argv) != num_args:
        logger(msg=f"🔥Not acceptable🔥 use {correct_command}")
        sys.exit(exit_code)

def input_(cast_to_int):
    # get input from user
    try:
        if cast_to_int:
            return int(input())
        else:
            return input()
    except:
        logger(msg="Not a valid INPUT. please try again!")
        

if __name__ == '__main__':
    # test
    logger('Hello World')
    