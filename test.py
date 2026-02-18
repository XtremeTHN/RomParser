import pathlib
from nxroms.fs.pfs0 import File
from nxroms.nacp import Nacp
from nxroms.nca.nca import Nca
from nxroms.rom.nsp import Nsp
from nxroms.rom.xci import Xci
from nxroms.fs.fs import FsType
from nxroms.nca.header import ContentType
from colorama import Fore, Style
import sys


def color(string, color):
    return color + str(string) + Fore.RESET


def colored(*msg, color=Fore.GREEN, level=""):
    print(color + Style.BRIGHT + str(level) + Style.RESET_ALL, *msg)


def color_ctx(prefix):
    def wrapper(*msg, color=Fore.GREEN, level=""):
        colored(*msg, color=color, level=str(prefix) + str(level))

    return wrapper


def info(*msg):
    colored(*msg, level="INFO")


def print_nca_filesystems(nca):
    c = color_ctx("Header ")
    for index, header in enumerate(nca.header.fs_headers):
        c("filesystem:", header.fs_type, level=header.index)
        c("hash type:", header.hash_type, level=header.index)
        c(
            "start_offset:",
            nca.header.fs_entries[index].start_offset,
            level=header.index,
        )
        c("end_offset:", nca.header.fs_entries[index].end_offset, level=header.index)
        print()


def print_nca_info(nca):
    if hasattr(nca, "entry"):
        info("nca:", nca.entry.name)

    info("rights id:", nca.header.rights_id)
    if hasattr(nca, "key_area"):
        info("key area:", nca.header.key_area)

    print()
    info("parsing filesystems in nca...")
    print_nca_filesystems(nca)


def print_all_ncas(rom):
    files = rom.get_files()

    print("-" * 50)
    for x in files:
        print_nca_info(x)
        print("-" * 50)


def control_nca(rom: Nsp):
    files = rom.get_files()

    for x in files:
        if x.header.content_type != ContentType.CONTROL:
            continue

        info("found control nca")
        print_nca_info(x)
        x.dump(x.entry.name)

        info("opening romfs")
        romfs = x.open_romfs(x.header.fs_headers[0])

        info("romfs header:", romfs.header)

        for f in romfs.files:
            c = color_ctx(f.name + ":")
            c(f"size {f.size} offset {f.offset}")

        print()

        for f in romfs.files:
            if f.name != "control.nacp":
                continue
            o = romfs.get_file(f)
            n = Nacp(o)

            t = n.titles[0]
            info("rom name:", t.name)
            info("rom publisher:", t.publisher)
            info("rom version:", n.version)

        break
    else:
        info("control nca not found")


def parse_nsp(f):
    p = Nsp(f)

    control_nca(p)


def parse_xci(f):
    x = Xci(f)

    info(x.header)


def parse_nca(f: pathlib.Path):
    file = File(f)
    x = Nca(file)

    print_nca_info(x)


def extract_bytes(f, offset, size):
    x = File(f)
    o = open("out.bin", "wb")
    o.write(x.read_at(offset, size))


if len(sys.argv) == 1:
    colored("pass a file to view its information", color=Fore.YELLOW, level="WARN")
    sys.exit(1)

FILE = pathlib.Path(sys.argv[1])

info("parsing", color(FILE, Fore.CYAN))
match FILE.suffix:
    case ".nsp":
        parse_nsp(FILE)
    case ".xci":
        parse_xci(FILE)
    case ".nca":
        parse_nca(FILE)
    case _:
        colored("invalid file", color=Fore.RED, level="ERROR")
        sys.exit(1)
