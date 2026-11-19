class Figurka:
    def __init__(self, nazev, vektory_utoku, barva, vektory, skok):
        self.nazev: str = nazev
        self.barva: bool = barva
        self.skok: bool
        self.aktivni: bool = True
        self.vektory_utoku: List[List[int]] = []
        self.vektory: List[List[int]] = []
#https://www.geeksforgeeks.org/python/python-object/