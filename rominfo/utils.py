from enum import Enum

class ByteEnum(Enum):
    def __init__(self, value):
        super().__init__(int.from_bytes(value))