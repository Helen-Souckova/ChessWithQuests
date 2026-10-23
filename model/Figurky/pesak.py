from model.figurka import Figurka


class Pesak(Figurka):
    def __init__(self, nazev, vektory_utoku, barva, vektory):
        super().__init__(nazev, vektory_utoku, barva, vektory)
