from argparse import ArgumentParser, SUPPRESS
import sys
import threading
import socket
import readchar
import time
from utils.packet_functions import *

# Chat Functions
# quit() or exit()
# members() or users()
# chat()
# message(NAME)

user_input = ""
cursor = 0
prompt = "Input"

def rtinput():
    global user_input
    global prompt
    global cursor
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
    time.sleep(0.4)
    print("",end="\n")
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    rtinput()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete

def continuously_send(connection, version):
    global user_input
    while True:
        try:
            type = MessageType.CHAT.value
            get_input()
            if user_input=="" or user_input==" ":
                continue
            elif user_input=="exit()" or user_input=="quit()":
                type = MessageType.COMMAND.value
                send_packet(connection, form_packet(version,type,user_input))
                break
            elif user_input=="members()" or user_input=="users()":
                type = MessageType.COMMAND.value
                send_packet(connection, form_packet(version,type,user_input))
                continue
            elif user_input=="chat()":
                type = MessageType.COMMAND.value
                send_packet(connection, form_packet(version,type,user_input))
                continue
            else:
                send_packet(connection, form_packet(version,type,user_input))
        except:
            quit()

def continuously_receive(connection):
    global user_input
    global prompt
    global cursor
    while True:
        try:
            packet = receive_packet(connection)
            print("",end='\n',flush=True)
            sys.stdout.write("\033[F"+"\033[K") #previous line and delete
            print(message_from_packet(packet))
            print("",end='\n',flush=True)
            sys.stdout.write("\033[F"+"\033[K") #previous line and delete
            print(f'{prompt}: {user_input}', end="", flush=True)
            if cursor < len(user_input):
                sys.stdout.write(u"\u001b[1000D")
                sys.stdout.write(u"\u001b[" + str(len(prompt)+2+cursor) + "C")
                sys.stdout.flush()
        except:
            quit()

def main():
    # Command line parser
    parser = ArgumentParser(add_help=False,description="Ping a port on a certain network")
    requiredArgs = parser.add_argument_group("required arguments")
    optionalArgs = parser.add_argument_group("optional arguments")
    # Adding All command line arguments
    requiredArgs.add_argument("-a","--address",required=True,help="the IP address of the server")
    requiredArgs.add_argument("-p","--port",required=True,help="the port of the server")
    optionalArgs.add_argument("-n","--name",required=False,help="the name you want to go by in chat")
    optionalArgs.add_argument("-h","--help",action="help",default=SUPPRESS,help="show this help message and exit")
    # Getting All arguments
    args = vars(parser.parse_args())
    # Relaying ALL arguments into variables
    address = args["address"]
    port = int(args["port"])

    # Client packet+message information
    version = 1
    if not args["name"]:
        name = input("Your Name: ")
        if len(name)>15 or len(name)<2:
            name = "Default"
    else:
        name = args["name"]

    try:
        # Socket setup
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, port))

        send_packet(s, form_packet(version,MessageType.SETUP.value,name))
        packet = receive_packet(s)
        sys.stdout.write("\033[F"+"\033[K") #previous line and delete
        print(f'Your name will be {message_from_packet(packet)} for the chat.\n')
        print(f'\tChat has been started.')

        # Chat Output
        output_thread = threading.Thread(target=continuously_receive, args=[s])
        output_thread.daemon = True
        output_thread.start()

        # Chat Input
        user_input_thread = threading.Thread(target=continuously_send, args=[s,version])
        user_input_thread.daemon = False
        user_input_thread.start()

        while True:
            if not user_input_thread.is_alive():
                print(f'\tChat has ended.')
                close_socket(s)
                break
        print(f'\nExiting Program')
        quit()

    except socket.error as err:
        quit()
    except KeyboardInterrupt:
        quit()
    except:
        quit()


if __name__ == '__main__':
    main()