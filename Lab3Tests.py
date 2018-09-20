from CS2911L3.Lab3Main import read_message
from CS2911L3.Message import Message


def message_test():
    message_bytes = b'\x00\x00\x00\x04\x4c\x61\x62\x20' \
                    b'\x31\x0a\x50\x68\x69\x6c\x65\x61' \
                    b'\x73\x20\x46\x6f\x67\x67\x0a\x0a' \
                    b'\x54\x68\x69\x73\x20\x69\x73\x20' \
                    b'\x6d\x79\x20\x6c\x61\x62\x20\x31' \
                    b'\x20\x61\x73\x73\x69\x67\x6e\x6d' \
                    b'\x65\x6e\x74\x2e\x0a'
    test_message = Message(message_bytes)
    lines = read_message(test_message)
    for i in lines:
        print(i.decode("ASCII"))


def empty_test():
    message_bytes = b'\x00\x00\x00\x00'
    test_message = Message(message_bytes)
    lines = read_message(test_message)
    for i in lines:
        print(i.decode("ASCII"))


print("Testing parsing given message:")
print("-----------------------------")
message_test()
print("-----------------------------\n")

print("Testing with message size 0:")
print("-----------------------------")
empty_test()
print("-----------------------------\n")
