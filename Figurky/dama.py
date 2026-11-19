from Game_core.figurka import Figurka


class Dama(Figurka):
    nazev = "Dama"
    zkratka = "D"
    hodnota = 9
    skok = False
    symboly = ("♕", "♛")