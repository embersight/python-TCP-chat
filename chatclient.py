from argparse import ArgumentParser, SUPPRESS
import sys
import threading
import socket

from packet_functions import *

# Chat Functions
# quit() or exit()
# members()

def user_input():
    print()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    response = input("Input: ")
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    return response

def continuously_send(connection, version):
    while True:
        type = MessageType.CHAT.value
        message = user_input()
        if message=="" or message==" ":
            continue
        if message=="exit()" or message=="quit()":
            type = MessageType.COMMAND.value
        send_packet(connection, form_packet(version,type,message))

def continuously_receive(connection):
    while True:
        packet = receive_packet(connection)
        print()
        sys.stdout.write("\033[F"+"\033[K") #previous line and delete
        print(message_from_packet(packet))
        print("Input: ", end='', flush=True)

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
    # Getting All arugments
    args = vars(parser.parse_args())
    # Relaying ALL arguments into variables
    address = args["address"]
    port = int(args["port"])

    # Client packet+message information
    version = 1
    if not args["name"]:
        name = input("Your Name: ")
        if len(name)>15:
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
        print(f'Your name will be named {message_from_packet(packet)} for the chat.\n')
        print(f'Chat has been started.')

        # Chat Output
        output_thread = threading.Thread(target=continuously_receive, args=[s])
        output_thread.daemon = False
        output_thread.start()

        # Chat Input
        user_input_thread = threading.Thread(target=continuously_send, args=[s,version])
        user_input_thread.daemon = False
        user_input_thread.start()

        while True:
            if not user_input_thread.is_alive():
                print(f'Chat has ended.')
                close_socket(s)
                break

    except socket.error as err:
        print(f'Socket failed with error {err}.')
    except KeyboardInterrupt:
        print(f'Socket connection manually closed.')
    except:
        print(f'Socket unknown error occured.')


if __name__ == '__main__':
    main()