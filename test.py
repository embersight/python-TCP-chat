import sys
import threading
import time
import readchar

user_input = ""
output_block = False

def rtinput(prompt):
    global user_input
    user_input = ""
    print(prompt,end="",flush=True)
    while True:
        key = readchar.readkey()
        if key==readchar.key.ENTER:
            print("",end="\n")
            break
        elif key==readchar.key.BACKSPACE:
            print("",end="\n")
            sys.stdout.write("\033[F"+"\033[K")
            user_input = user_input[:-1]
            print(f'{prompt+user_input}',end="",flush=True)
        elif ord(key)>=32:
            print(key,end="",flush=True)
            user_input += key
        else:
            pass

def get_input():
    print()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    rtinput("Input: ")
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete

def continuously_send():
    global user_input
    while True:
        get_input()
        print("User: "+user_input)

def continuously_receive():
    global user_input
    while True:
        time.sleep(1)
        print("",end='\n',flush=True)
        sys.stdout.write("\033[F"+"\033[K") #previous line and delete
        print("Some Output has been displayed.",flush=False)
        print("",end='\n',flush=True)
        sys.stdout.write("\033[F"+"\033[K") #previous line and delete
        print("Input: "+user_input, end='', flush=True)

def main():
    print(f'Starting Application')

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

if __name__ == '__main__':
    main()