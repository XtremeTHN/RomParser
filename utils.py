import mmap
import struct
from typing import Any
from abc import ABC, abstractmethod

class IReadable(ABC):
    @abstractmethod
    def tell(self) -> int:
        ...

    @abstractmethod
    def seek(self, offset: int) -> None:
        ...
    
    @abstractmethod
    def read(self, size: int) -> bytes | None:
        ...
    
    @abstractmethod
    def read_at(self, offset: int, size: int) -> bytes:
        ...
    
    @abstractmethod
    def read_to(self, offset: int, size: int, format_string: str) -> Any:
        ...

class Readable(IReadable):
    def __init__(self, obj: IReadable):
        self.obj = obj
    
    def seek(self, offset: int):
        self.obj.seek(offset)

    def tell(self) -> int:
        return self.obj.tell()

    def fileno(self) -> int:
        return self.obj.fileno()
    
    def read(self, size: int):
        return self.obj.read(size)

    def read_at(self, offset: int, size: int):
        return self.obj.read_at(offset, size)

    def read_to(self, offset: int, size: int, format_string: str):
        return struct.unpack(format_string, self.read_at(offset, size))[0]

class File(Readable):
    def __init__(self, file: str):
        self.obj = open(file, "rb")

    def read_at(self, offset: int, size: int):
        self.seek(offset)
        return self.obj.read(size)


class OutOfBounds(Exception):
    ...

class Region(Readable):
    def __init__(self, source: IReadable, offset: int, end: int):
        super().__init__(source)
        self.offset = offset
        self.end = end

    def calc_offset(self, offset: int):
        total_offset = self.offset + offset
        if (total_offset > self.end):
            raise OutOfBounds(f"maximum: {self.end}, provided offset: {offset}, offset: {self.offset}")
        return total_offset

    def seek(self, offset):
        super().seek(self.calc_offset(offset))
    
    def read(self, size: int):
        current_pos = self.obj.tell() - self.offset
        remaining_bytes = self.end - current_pos

        if remaining_bytes <= 0:
            return None

        read_size = min(size, remaining_bytes)
        return super().read(read_size)
    
    def read_at(self, offset, size):
        return super().read_at(self.calc_offset(offset), size)

    def read_to(self, offset, size, format_string):
        return super().read_to(self.calc_offset(offset), size, format_string)