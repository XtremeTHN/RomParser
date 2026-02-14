from readers import IReadable, Readable
from dataclasses import dataclass
import struct

@dataclass
class Romfs(Readable):
    header_size: int
    dir_hash_table_offset: int
    dir_hash_table_size: int
    dir_meta_table_offset: int
    dir_meta_table_size: int
    file_hash_table_offset: int
    file_hash_table_size: int
    file_meta_table_offset: int
    file_meta_table_size: int
    data_offset: int

    def __init__(self, source: IReadable):
        super().__init__(source)
        self.populate_header()

    def populate_header(self):
        self.header_size = self._read_to(0x8, "<Q")
        self.dir_hash_table_offset = self._read_to(0x8, "<Q")
        self.dir_hash_table_size = self._read_to(0x8, "<Q")
        self.dir_meta_table_offset = self._read_to(0x8, "<Q")
        self.dir_meta_table_size = self._read_to(0x8, "<Q")
        self.file_hash_table_offset = self._read_to(0x8, "<Q")
        self.file_hash_table_size = self._read_to(0x8, "<Q")
        self.file_meta_table_offset = self._read_to(0x8, "<Q")
        self.file_meta_table_size = self._read_to(0x8, "<Q")
        self.data_offset = self._read_to(0x8, "<Q")