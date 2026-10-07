@dataclass
class Hrac:
    barva: int
    uzivatel: Uzivatel

    def getEloRating(self) -> int:
        return self.uzivatel.elo