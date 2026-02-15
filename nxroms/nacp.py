from enum import IntEnum
from dataclasses import dataclass
from .readers import IReadable, Readable, MemoryRegion
from .utils import strip


class TitleLanguage(IntEnum):
    AMERICAN_ENGLISH = 0
    BRITISH_ENGLISH = 1
    JAPANESE = 2
    FRENCH = 3
    GERMAN = 4
    LATIN_AMERICAN_SPANISH = 5
    SPANISH = 6
    ITALIAN = 7
    DUTCH = 8
    CANADIAN_FRENCH = 9
    PORTUGUESE = 10
    RUSSIAN = 11
    KOREAN = 12
    TRADITIONAL_CHINESE = 13
    SIMPLIFIED_CHINESE = 14
    BRAZILIAN_PORTUGUESE = 15


@dataclass
class Title:
    language: TitleLanguage
    name: str
    publisher: str

    def __init__(self, data: bytes, index: int):
        self.language = TitleLanguage(index)
        m = MemoryRegion(data)

        self.name = strip(m.read(0x200))
        self.publisher = strip(m.read(0x100))


class Nacp(Readable):
    titles: list[Title]
    version: int

    def __init__(self, source: IReadable):
        super().__init__(source)

        self.titles = []

        for x in range(16):
            t = Title(self.read(0x300), x)
            if t.name == "" or t.publisher == "":
                continue
            self.titles.append(t)

        self.version = strip(source.read_at(0x3060, 0x10))
