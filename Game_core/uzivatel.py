from Game_core.kwest import Kwest
from typing import List

class Uzivatel:
    def __init__(self, uzivatelske_jmeno: str, jmeno: str, email: str, elo: int = 1200):
        self.uzivatelske_jmeno = uzivatelske_jmeno
        self.jmeno = jmeno
        self.email = email
        self.elo = elo
        self.splnene_kwesty: List[Kwest] = []

    def pridej_kwest(self, kwest: Kwest) -> None:
        if kwest in self.splnene_kwesty:
            return
        kwest.spln()
        self.splnene_kwesty.append(kwest)
        self.elo += int(kwest.odmena_xp / 10)