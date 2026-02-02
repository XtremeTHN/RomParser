from rom import Nsp

p = Nsp("undertale.nsp")
p.populate_attrs()

print(
    "partition_entry_count:", p.partition_entry_count,
    "string_table_size:", p.string_table_size,
    "reserved:", p.reserved
)

for x in p.get_ncas():
    print(x.name, x.entry.size)
    n = open(f"out/{x.name}", "wb")
    
    while True:
        chunk = x.read(1024)
        if not chunk:
            print("end", x.entry.offset, x.entry.size, x.tell())
            break

        n.write(chunk)