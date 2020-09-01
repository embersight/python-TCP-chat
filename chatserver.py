from argparse import ArgumentParser, SUPPRESS
import socket
import logging
import threading
import time

from packet_functions import *

def new_client(connection_list, version, clientsocket, address):
    try:
        packet = receive_packet(clientsocket)
        name = message_from_packet(packet)
        if version_from_packet(packet)!=version:
            connection_list.pop((clientsocket,address))
            exit()
        if message_type_from_packet(packet)==MessageType.SETUP.value:
            number = 0
            for key in connection_list:
                if connection_list[key]==name:
                    number = number+1
            if number!=0:
                name = name+str(number)
        else:
            exit()

        connection_list[(clientsocket,address)] = name
        send_packet(clientsocket, form_packet(version, MessageType.SETUP.value, name))
        time.sleep(0.5)
        for connection in connection_list:
            send_packet(connection[0], form_packet(version, MessageType.CHAT.value, f'{name} has entered the chat.'))

        while True:
            packet = receive_packet(clientsocket)
            if message_type_from_packet(packet)==MessageType.CHAT.value:

                logging.info(f'{name} said "{message_from_packet(packet)}".')
                for connection in connection_list:
                    send_packet(connection[0], form_packet(version, MessageType.CHAT.value, f'{name}: {message_from_packet(packet)}'))

            elif message_type_from_packet(packet)==MessageType.COMMAND.value:

                if(message_from_packet(packet)=="quit()" or message_from_packet(packet)=="exit()"):
                    logging.info(f'Connection from {address} has been withdrawn.')
                    connection_list.pop((clientsocket,address))
                    for connection in connection_list:
                        send_packet(connection[0], form_packet(version, MessageType.CHAT.value, f'{name} has left the chat'))
                    exit()

            else:
                pass
    except:
        logging.info(f'Connection from {address} has been withdrawn.')
        connection_list.pop((clientsocket,address))
        exit()

def main():
    # Command Line Parser
    parser = ArgumentParser(add_help=False,description="Listen to a port on the current network")
    requiredArgs = parser.add_argument_group("required arguments")
    optionalArgs = parser.add_argument_group("optional arguments")
    # Adding All Command Line Arguments
    requiredArgs.add_argument("-p","--port",required=True,help="the port server listens on")
    requiredArgs.add_argument("-l","--logfile",required=True,help="where it will keep a record of actions")
    optionalArgs.add_argument("-h","--help",action="help",default=SUPPRESS,help="show this help message and exit")
    # Getting All Arugments
    args = vars(parser.parse_args())

    # Relaying ALL Arguments into Variables
    port = int(args["port"])
    logpath = str(args["logfile"])

    # Logging Setup
    logging.basicConfig(level=logging.NOTSET,filename=logpath,filemode='w',format='%(asctime)s.%(msecs)03d | %(levelname)s: %(message)s',datefmt='%d-%B-%Y %H:%M:%S')

    # Server Setup
    version = 1

    try:
        # Socket setup
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f'Socket successfully created.')
        s.bind((socket.gethostname(), port))
        logging.info(f'Socket binded to {port}.')
        s.listen(10)
        logging.info(f'Socket is listening.')

        connection_list = {}
        while True:
            try:
                # Connect with a client
                c, addr = s.accept()
                connection_list[(c,addr)] = "NOTSET"
                logging.info(f'Connection from {addr} has been established.')

                user_input_thread = threading.Thread(target=new_client, args=[connection_list,version,c,addr])
                user_input_thread.daemon = False
                user_input_thread.start()

            except (BlockingIOError, InterruptedError, ConnectionAbortedError):
                pass

        close_socket(s)
        logging.info(f'Socket is closed.')

    except socket.error as err:
        logging.error(f'Socket failed with error {err}.')
    except socket.herror:
        logging.error(f'Socket failed with an address herror.')
    except socket.gaierror:
        logging.error(f'Socket failed with an address gaierror.')
    except socket.timeout:
        logging.error(f'Socket failed with a timeout error.')
    except KeyboardInterrupt:
        logging.error(f'Socket connection manually closed.')
    except:
        logging.error(f'Socket unknown error occured.')

if __name__ == '__main__':
    main()