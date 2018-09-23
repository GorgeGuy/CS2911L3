"""
- CS2911 - 021
- Fall 2018
- Lab 3 - Parser Design
- Names:
  - Joshua Spleas
  - Seth Fenske

    A data parser for an imaginary message format
"""

from CS2911L3.Message import Message

def print_to_file(list_of_lines, file_path):
    """
    Prints the message cointainted in list_of_lines to the file at the specified path.

    :param list_of_lines: A list containing each line of text to write to the file as a respecstive entry.
    :param file_path:  The full path that points to the file to which we will write
    :return: None
    """
    with open(file_path) as output_file:
        write_lines(list_of_lines, output_file)

def get_file_name():
    """
    Prompts the user for the name of a file they would like to write the results to.
    :return: The full path of the file they are trying to write to
    """
    file_name = input("Please enter the name of the file you would like to write to: ")
    return file_name


def read_message(message):
    """
    Reads the passed message to a list of bytes

    :param message: the message object implementing the next_byte method
    :return: list of bytes where each element is a line from the file
    :author: Joshua Spleas
    """
    found_lines = list()
    num_lines = read_num_lines(message)
    for i in range(0,num_lines):
        found_lines.append(read_next_line(message))

    return found_lines

def read_num_lines(message):
    """
    Reads four bytes from the message as a single integer value
    :param message: the message to read from
    :return: the number of lines
    :author: Joshua Spleas
    """
    size_bytes = b''
    for i in range(0, 4):
        size_bytes += message.next_byte()
    return int.from_bytes(size_bytes, 'big')

def read_next_line(message):
    """
    Reads bytes from a message until a newline (0x0a) byte is read
    :param message: message to read from
    :return: a byte string for the line, not including any newline characters
    :author: Joshua Spleas
    """
    current_byte = message.next_byte()
    found_line = b''
    while current_byte != b'\x0a':
        found_line += current_byte
        current_byte = message.next_byte()
    return found_line

def write_lines(list_of_linse, file):
    """
    Writes the list_of_lines to the given file.
    :param list_of_linse: The lines to be added to the file
    :param file: The file to which we will write
    :return: None
    """
    for i in range(0, len(list_of_linse)):
        file.write(list_of_linse[i] + "\n")

def main():
    message = Message(b'\x00\x00\x00\x05'
                      b'This is a test message\x0a'
                      b'This is a second line\x0a'
                      b'\x0a'
                      b'\x0a'
                      b'This is a line after 2 were skipped\x0a')
    lines = read_message(message)
    #TODO add file writing and remove print
    for i in lines:
        print(i)

main()
