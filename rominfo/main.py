from rom import Nsp
from nca import Nca

p = Nsp("undertale.nsp")
p.populate_attrs()

print(
    "partition_entry_count:", p.partition_entry_count,
    "string_table_size:", p.string_table_size,
    "reserved:", p.reserved
)

files = p.get_files()
for index, value in enumerate(files):
    print(index, value.magic)

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
