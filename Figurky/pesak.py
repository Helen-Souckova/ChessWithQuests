from Game_core.figurka import Figurka
from core import BILY


class Pesak(Figurka):
    nazev = "Pesak"
    zkratka = ""
    hodnota = 1
    skok = False
    symboly = ("♙", "♟")

    @property
    def vychozi_radka(self) -> int:
        return 6 if self.barva == BILY else 1