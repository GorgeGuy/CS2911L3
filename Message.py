"""
- CS2911 - 021
- Fall 2018
- Lab 3 - Parser Design
- Names:
  - Joshua Spleas
  - Seth Fenske

    A simple wrapper for a bytes object that implements a next_bytes method
"""
class Message:

    bytes_ = b'test'
    last_index_ = 0

    def __init__(self, new_bytes):
        """
        constructor for message object
        :param new_bytes: bytes to store
        """
        self.bytes_ = new_bytes

    def next_byte(self):
        """
        Method to get the next byte, prints message to console if no next byte
        :return: next unread byte of the message, or 0xDEADBEEF if none
        """
        if self.last_index_ == len(self.bytes_):
            print('end of message')
            return b'\xDE\xAD\xBE\xEF'
        result = self.bytes_[self.last_index_].to_bytes(1, 'big')
        self.last_index_ += 1
        return result