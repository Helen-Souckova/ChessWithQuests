from model.Figurky.pozice import Pozice
from model.figurka import Figurka


class Dama(Figurka, Pozice):
    def __init__(self, nazev, vektory_utoku, barva, vektory, pozice):
        super().__init__(nazev, vektory_utoku, barva, vektory, pozice)
