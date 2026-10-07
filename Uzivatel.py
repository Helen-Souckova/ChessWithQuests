@dataclass
class Uzivatel:
    uzivatelske_jmeno: str
    jmeno: str
    email: str
    elo: int = 1200
    splnene_questy: list[Quest] = field(default_factory=list)

    def pridej_quest(self, quest: Quest):
        self.splnene_questy.append(quest)