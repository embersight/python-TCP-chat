import socket
import struct
from enum import Enum
from cryptography.fernet import Fernet

class MessageType(Enum):
    SETUP    = 0
    COMMAND  = 1
    CHAT     = 2

def close_socket(connection):
    try:
        connection.shutdown(socket.SHUT_RDWR)
    except:
        pass
    try:
        connection.close()
    except:
        pass

def form_packet(version, message_type, message, key):
    body = bytes(message, 'utf-8')
    if key!="":
        f = Fernet(key)
        body = f.encrypt(body)
    head = struct.pack("IiI", version, message_type, len(body))
    return (head+body)

def version_from_packet(packet):
    version, message_type, message_length = struct.unpack("IiI", packet[:struct.calcsize("IiI")])
    return version

def message_type_from_packet(packet):
    version, message_type, message_length = struct.unpack("IiI", packet[:struct.calcsize("IiI")])
    return message_type

def message_from_packet(packet, key):
    version, message_type, message_length = struct.unpack("IiI", packet[:struct.calcsize("IiI")])
    message = packet[struct.calcsize("IiI"):]
    if key!="":
        f = Fernet(key)
        message = f.decrypt(message)
    return (message.decode("utf-8"))

def send_packet(connection, packet):
    connection.send(packet)

def receive_packet(connection):
    head = connection.recv(12)
    version, message_type, message_length = struct.unpack("IiI", head)
    body = connection.recv(message_length)
    return (head+body)