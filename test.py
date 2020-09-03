import sys
import threading
import time
import readchar


def user_input():
    print()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    response = input("Input: ")
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    return response

def continuously_send():
    while True:
        message = user_input()
        print("User: "+message)

def continuously_receive():
    while True:
        time.sleep(1)
        print("",end='\n',flush=True)
        sys.stdout.write("\033[F"+"\033[K") #previous line and delete
        print("Some Output has been displayed.")
        print("Input: ", end='', flush=True)

def rtinput(prompt):
    string = ""
    print(f'{prompt}',end="",flush=True)
    while True:
        key = readchar.readkey()
        if key==readchar.key.ENTER
            print("",end="\n",flush=True)
            break
        elif key==readchar.key.BACKSPACE:
            print("",end="\n",flush=True)
            sys.stdout.write("\033[F"+"\033[K")
            string = string[:-1]
            print(prompt+string,end="",flush=True)
        elif ord(key)>=32:
            print(key,end="",flush=True)
            string += key
        else:
            pass
    return string

def main():
    print(f'Starting Application')
    answer = rtinput("Input: ")
    print(f'{answer}')

    """
    # Chat Input
    user_input_thread = threading.Thread(target=continuously_send, args=[])
    user_input_thread.daemon = True
    user_input_thread.start()

    # Chat Output
    output_thread = threading.Thread(target=continuously_receive, args=[])
    output_thread.daemon = True
    output_thread.start()



    while True:
        if not user_input_thread.is_alive():
            print(f'\nExiting Application')
            break
    """
if __name__ == '__main__':
    main()