import socket
import struct

def close_socket(connection):
    try:
        connection.shutdown(socket.SHUT_RDWR)
    except:
        pass
    try:
        connection.close()
    except:
        pass

def form_packet(version, message_type, message):
    body = bytes(message, 'utf-8')
    head = struct.pack("IiI", version, message_type, len(body))
    packet = head+body
    return packet

def version_from_packet(packet):
    version, message_type, message_length = struct.unpack("IiI", packet[:struct.calcsize("IiI")])
    return version

def message_type_from_packet(packet):
    version, message_type, message_length = struct.unpack("IiI", packet[:struct.calcsize("IiI")])
    return message_type

def message_from_packet(packet):
    message = packet[12:].decode("utf-8")
    return message

def send_packet(connection, packet):
    connection.send(packet)

def receive_packet(connection):
    head = connection.recv(12)
    version, message_type, message_length = struct.unpack("IiI", head)
    body = connection.recv(message_length)
    return (head+body)


"""
def receive_packet(connection):
    amount_received = 0
    amount_expected = struct.calcsize("IiI")

    head = b''
    while amount_received < amount_expected:
        data = connection.recv(12)
        amount_received += len(data)
        if len(data)>0:
            head += data

    version, message_type, message_length = struct.unpack("IiI", head)
    body = connection.recv(message_length)
    return (head+body)
"""