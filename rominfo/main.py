from rom import Nsp
from nca import ContentType, FsType
from colorama import Fore, Style

def color(string, color):
    return color + string + Fore.RESET

def colored(*msg, color=Fore.GREEN, level=""):
    print(color + Style.BRIGHT + str(level) + Style.RESET_ALL, *msg)

def color_ctx(prefix):
    def wrapper(*msg, color=Fore.GREEN, level=""):
        colored(*msg, color=color, level=str(prefix) + str(level))

    return wrapper         

def info(*msg):
    colored(*msg, level="INFO")

FILE = "undertale.nsp"

info("parsing", color(FILE, Fore.CYAN))
p = Nsp(FILE)
p.populate_attrs()

files = p.get_files()

print("-" * 50)
for x in files:
    info("nca:", x.name)
    info("rights id:", x.rights_id)
    if hasattr(x, "key_area"):
        info("key area:", x.key_area)

    info("parsing filesystems in nca...\n")

    c = color_ctx("Header ")
    for index, header in enumerate(x.fs_headers):
        c("filesystem:", header.fs_type, level=header.index)
        c("hash type:", header.hash_type, level=header.index)
        c("start_offset:", x.fs_entries[index].start_offset, level=header.index)
        c("end_offset:", x.fs_entries[index].end_offset, level=header.index)
        print()

    print("-" * 50)
        # f = x.open_romfs(x.fs_headers[0])
        # colored(f, level=header.index)
        
# print(file.content_type, file.content_size)

# for x in file.fs_entries:
#     print(x, x.start_offset, x.end_offset)

# for x in file.fs_headers:
#     print(x)
# print(file.fs_entries[1].start_offset, file.fs_entries[1].end_offset)
# file.decrypted_header.dump(f"{file.name}.bin")

# file.get_fs_header_for_section(0
# file.populate_fs_entries()

# for x in p.get_files():
#     print(x.name, x.entry.size)
#     n = open(f"out/{x.name}", "wb")
    
#     while True:
#         chunk = x.read(1024)
#         if not chunk:
#             print("end", x.entry.offset, x.entry.size, x.tell())
#             break

#         n.write(chunk)
#         del chunk
