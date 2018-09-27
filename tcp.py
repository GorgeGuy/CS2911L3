"""
- CS2911 - 0NN
- Fall 2018
- Lab 4
- Names:
  - Joshua Spleas
  - Seth Fenske

A simple TCP server/client pair.

The application protocol is a simple format: For each file uploaded, the client first sends four (big-endian) bytes indicating the number of lines as an unsigned binary number.

The client then sends each of the lines, terminated only by '\\n' (an ASCII LF byte).

The server responds with 'A' if it accepts the file, and 'R' if it rejects it.

Then the client can send the next file.
"""

# import the 'socket' module -- not using 'from socket import *' in order to selectively use items with 'socket.' prefix
import socket
import struct
import time
import sys

# Port number definitions
# (May have to be adjusted if they collide with ports in use by other programs/services.)
TCP_PORT = 12100

# Address to listen on when acting as server.
# The address '' means accept any connection for our 'receive' port from any network interface
# on this system (including 'localhost' loopback connection).
LISTEN_ON_INTERFACE = ''

# Address of the 'other' ('server') host that should be connected to for 'send' operations.
# When connecting on one system, use 'localhost'
# When 'sending' to another system, use its IP address (or DNS name if it has one)
# OTHER_HOST = '155.92.x.x'
OTHER_HOST = 'localhost'


def main():
    """
    Allows user to either send or receive bytes
    """
    # Get chosen operation from the user.
    action = input('Select "(1-TS) tcpsend", or "(2-TR) tcpreceive":')
    # Execute the chosen operation.
    if action in ['1', 'TS', 'ts', 'tcpsend']:
        tcp_send(OTHER_HOST, TCP_PORT)
    elif action in ['2', 'TR', 'tr', 'tcpreceive']:
        tcp_receive(TCP_PORT)
    else:
        print('Unknown action: "{0}"'.format(action))


def tcp_send(server_host, server_port):
    """
    - Send multiple messages over a TCP connection to a designated host/port
    - Receive a one-character response from the 'server'
    - Print the received response
    - Close the socket
    
    :param str server_host: name of the server host machine
    :param int server_port: port number on server to send to
    """
    print('tcp_send: dst_host="{0}", dst_port={1}'.format(server_host, server_port))
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((server_host, server_port))

    num_lines = int(input('Enter the number of lines you want to send (0 to exit):'))

    while num_lines != 0:
        print('Now enter all the lines of your message')
        # This client code does not completely conform to the specification.
        #
        # In it, I only pack one byte of the range, limiting the number of lines this
        # client can send.
        #
        # While writing tcp_receive, you will need to use a different approach to unpack to meet the specification.
        #
        # Feel free to upgrade this code to handle a higher number of lines, too.
        tcp_socket.sendall(b'\x00\x00')
        time.sleep(1)  # Just to mess with your servers. :-)
        tcp_socket.sendall(b'\x00' + bytes((num_lines,)))

        # Enter the lines of the message. Each line will be sent as it is entered.
        for line_num in range(0, num_lines):
            line = input('')
            tcp_socket.sendall(line.encode() + b'\n')

        print('Done sending. Awaiting reply.')
        response = tcp_socket.recv(1)
        if response == b'A':  # Note: == in Python is like .equals in Java
            print('File accepted.')
        else:
            print('Unexpected response:', response)

        num_lines = int(input('Enter the number of lines you want to send (0 to exit):'))

    tcp_socket.sendall(b'\x00\x00')
    time.sleep(1)  # Just to mess with your servers. :-)  Your code should work with this line here.
    tcp_socket.sendall(b'\x00\x00')
    response = tcp_socket.recv(1)
    if response == b'Q':  # Reminder: == in Python is like .equals in Java
        print('Server closing connection, as expected.')
    else:
        print('Unexpected response:', response)

    tcp_socket.close()


def tcp_receive(listen_port):
    """
    - Listen for a TCP connection on a designated "listening" port
    - Accept the connection, creating a connection socket
    - Print the address and port of the sender
    - Repeat until a zero-length message is received:
      - Receive a message, saving it to a text-file (1.txt for first file, 2.txt for second file, etc.)
      - Send a single-character response 'A' to indicate that the upload was accepted.
    - Send a 'Q' to indicate a zero-length message was received.
    - Close data connection.
   
    :param int listen_port: Port number on the server to listen on
    """

    print('tcp_receive (server): listen_port={0}'.format(listen_port))
    # Replace this comment with your code.

    data_socket = init_setver()

    handle_messages(data_socket)

    data_socket.close()


def init_setver(listen_port):
    """
    Creates a new socket to listen for messages.
    :param listen_port: The port that you want the socket to listen on
    :author: Seth Fenske
    :return: The TCP socket recieving the data
    """
    tcp_server = socket.socket(listen_port, socket.SOCK_STREAM)
    tcp_server.bind(listen_port)
    return tcp_server

def handle_messages(data_socket):
    """
    Method to handle reading messages from a client
    After every message is received, an 'A' byte is sent and a file is saved
    After an empty message is received, a 'Q' byte is sent
    :param data_socket: active tcp socket to recieve/send from
    :return: None
    """
    size = 1
    message_number = 1
    while size != 0:
        lines = read_message(data_socket)
        size = len(lines)
        if size != 0:
            file_name = str(message_number) + ".txt"
            message_number += 1
            with open(file_name, "wb") as file:
                write_lines(lines, file)
            data_socket.sendall(b'A')
    data_socket.sendall(b'Q')



def next_byte(data_socket):
    """
    Read the next byte from the socket data_socket.

    Read the next byte from the sender, received over the network.
    If the byte has not yet arrived, this method blocks (waits)
      until the byte arrives.
    If the sender is done sending and is waiting for your response, this method blocks indefinitely.

    :param data_socket: The socket to read from. The data_socket argument should be an open tcp
                        data connection (either a client socket or a server data socket), not a tcp
                        server's listening socket.
    :return: the next byte, as a bytes object with a single byte in it
    """
    return data_socket.recv(1)

def print_to_file(list_of_lines, file_path):
    """
    Prints the message cointainted in list_of_lines to the file at the specified path.

    :param list_of_lines: A list containing each line of text to write to the file as a respecstive entry.
    :param file_path:  The full path that points to the file to which we will write
    :return: None
    :author: Seth Fenske
    """
    with open(file_path) as output_file:
        write_lines(list_of_lines, output_file)

def get_file_name():
    """
    Prompts the user for the name of a file they would like to write the results to.
    :return: The full path of the file they are trying to write to
    :author: Seth Fenske
    """
    file_name = input("Please enter the name of the file you would like to write to: ")
    return file_name


def read_message(data_socket):
    """
    Reads the passed message to a list of bytes

    :param message: the message object implementing the next_byte method
    :return: list of bytes where each element is a line from the file
    :author: Joshua Spleas
    """
    found_lines = list()
    num_lines = read_num_lines(data_socket)
    for i in range(0,num_lines):
        found_lines.append(read_next_line(data_socket))

    return found_lines

def read_num_lines(data_socket):
    """
    Reads four bytes from the message as a single integer value
    :param message: the message to read from
    :return: the number of lines
    :author: Joshua Spleas
    """
    size_bytes = b''
    for i in range(0, 4):
        size_bytes += next_byte(data_socket)
    return int.from_bytes(size_bytes, 'big')

def read_next_line(data_socket):
    """
    Reads bytes from a message until a newline (0x0a) byte is read
    :param message: message to read from
    :return: a byte string for the line, not including any newline characters
    :author: Joshua Spleas
    """
    current_byte = next_byte(data_socket)
    found_line = b''
    while current_byte != b'\x0a':
        found_line += current_byte
        current_byte = next_byte(data_socket)
    return found_line

def write_lines(list_of_lines, file):
    """
    Writes the list_of_lines to the given file.
    :param list_of_lines: The lines to be added to the file
    :param file: The file to which we will write
    :return: None
    :author: Seth Fenske
    """
    for i in range(0, len(list_of_lines)):
        file.write(list_of_lines[i] + b"\n")


# Invoke the main method to run the program.
main()
