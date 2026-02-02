from fs import PFS0
from readers import File
from nca import Nca

class Nsp(PFS0):
    def __init__(self, file: str):
        f = File(file)
        super().__init__(f)

    def get_nca(self, index: int) -> Nca:
        return Nca(super().get_file(index))

    def get_ncas(self) -> list[Nca]:
        return [Nca(x) for x in super().get_files()]