from argparse import ArgumentParser, SUPPRESS
import sys
import threading
import socket
import readchar

from packet_functions import *

# Chat Functions
# quit() or exit()
# members() or users()

def rtinput(prompt, user_input):
    user_input = ""
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

def get_input(user_input):
    print()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    response = rtinput("Input: ",user_input)
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    return response

def continuously_send(connection, version, user_input):
    while True:
        try:
            type = MessageType.CHAT.value
            message = get_input(user_input)
            if message=="" or message==" ":
                continue
            elif message=="exit()" or message=="quit()":
                type = MessageType.COMMAND.value
                send_packet(connection, form_packet(version,type,message))
                break
            elif message=="members()" or message=="users()":
                type = MessageType.COMMAND.value
                send_packet(connection, form_packet(version,type,message))
                continue
            else:
                pass

            send_packet(connection, form_packet(version,type,message))
        except:
            quit()

def continuously_receive(connection, user_input):
    while True:
        try:
            packet = receive_packet(connection)
            print("",end='\n',flush=True)
            sys.stdout.write("\033[F"+"\033[K") #previous line and delete
            print(message_from_packet(packet))
            print("Input: "+user_input, end='', flush=True)
        except:
            quit()

def main():
    print(f'Starting Application')

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

        user_input = ""

        # Chat Output
        output_thread = threading.Thread(target=continuously_receive, args=[s, user_input])
        output_thread.daemon = True
        output_thread.start()

        # Chat Input
        user_input_thread = threading.Thread(target=continuously_send, args=[s,version,user_input])
        user_input_thread.daemon = False
        user_input_thread.start()

        while True:
            if not user_input_thread.is_alive():
                print(f'\tChat has ended.')
                close_socket(s)
                break
        print(f'\nExiting Application')
        quit()

    except socket.error as err:
        quit()
    except KeyboardInterrupt:
        quit()
    except:
        quit()


if __name__ == '__main__':
    main()