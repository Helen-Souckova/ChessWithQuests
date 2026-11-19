from Game_core.pozice import Pozice
from core import BILY, nazev_barvy


class Figurka:
    nazev = "Figurka"
    zkratka = ""
    hodnota = 0
    skok = False
    symboly = ("?", "?")

    def __init__(self, barva: int, pozice: Pozice):
        self.barva = barva
        self.pozice = pozice
        self.pocet_tahu = 0
        self.aktivni = True

    @property
    def symbol(self) -> str:
        return self.symboly[self.barva]

    @property
    def smer(self) -> int:
        return -1 if self.barva == BILY else 1

    def __repr__(self) -> str:
        return f"{self.nazev}({nazev_barvy(self.barva)}, {self.pozice.na_alg()})"
