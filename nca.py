from entry import PartitionEntry
from fs import PFSItem
from readers import Readable

class Nca(Readable):
    name: str
    entry: PartitionEntry

    def __init__(self, item: PFSItem):
        super().__init__(item)

        self.name = item.name
        self.entry = item.entry
    
    # TODO: make a constructor that takes a file and parse it