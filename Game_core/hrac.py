from Game_core.uzivatel import Uzivatel


class Hrac:
    def __init__(self, barva: int, uzivatel: Uzivatel):
        self.barva = barva
        self.uzivatel = uzivatel

    def getEloRating(self) -> int:
        return self.uzivatel.elo