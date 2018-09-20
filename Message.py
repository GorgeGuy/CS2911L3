class Message:
    bytes_ = b'test'
    last_index = 0

    def __init__(self, new_bytes):
        self.bytes_ = new_bytes

    def next_byte(self):
        if self.last_index == len(self.bytes_):
            print('end of message')
            return b'\x00'
        result = self.bytes_[self.last_index].to_bytes(1, 'big')
        self.last_index += 1
        return result