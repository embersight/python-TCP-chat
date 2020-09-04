import sys
import readchar
import time

user_input = ""
prompt = "Input"


def rtinput():
    global user_input
    global prompt
    cursor = 0
    past_cursor = 0
    print(f'{prompt}: ',end="",flush=True)
    while True:
        key = readchar.readkey()
        if key==readchar.key.ENTER:
            print("",end="\n")
            break
        elif key==readchar.key.BACKSPACE:
            print("",end="\n")
            sys.stdout.write("\033[F"+"\033[K")
            user_input = user_input[0 : cursor-1 : ] + user_input[cursor-1 + 1 : :]
            cursor = max(0, cursor-1)
            print(f'{prompt}: {user_input}',end="",flush=True)
            if cursor < len(user_input):
                sys.stdout.write(u"\u001b[1000D")
                sys.stdout.write(u"\u001b[" + str(len(prompt)+2+cursor) + "C")
                sys.stdout.flush()
            continue
        elif key==readchar.key.LEFT:
            past_cursor = cursor
            cursor = max(0, cursor-1)
            if cursor!=past_cursor:
                sys.stdout.write(u"\u001b[1D")
                sys.stdout.flush()
            continue
        elif key==readchar.key.RIGHT:
            past_cursor = cursor
            cursor = min(len(user_input), cursor+1)
            if cursor!=past_cursor:
                sys.stdout.write(u"\u001b[1C")
                sys.stdout.flush()
            continue
        else:
            try:
                if(ord(key)>=32):
                    user_input = user_input[:cursor]+key+user_input[cursor:]
                    cursor += 1
                    print("",end="\n",flush=True)
                    sys.stdout.write("\033[F"+"\033[K")
                    print(f'{prompt}: {user_input}',end="",flush=True)
                    if cursor < len(user_input):
                        sys.stdout.write(u"\u001b[1000D")
                        sys.stdout.write(u"\u001b[" + str(len(prompt)+2+cursor) + "C")
                        sys.stdout.flush()
                    continue
            except:
                pass

def get_input():
    global user_input
    user_input = ""
    time.sleep(0.2)
    print("",end="\n")
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    rtinput()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete

def main():
    get_input()

if __name__ == '__main__':
    main()