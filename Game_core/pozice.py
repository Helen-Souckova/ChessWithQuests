from core import SLOUPCE, RADKY


class Pozice:
    """Pole sachovnice. radka 0 = 8. rada (cerna zakladna), sloupec 0 = 'a'."""

    __slots__ = ("radka", "sloupec")

    def __init__(self, radka: int, sloupec: int):
        self.radka = radka
        self.sloupec = sloupec

    def to_tuple(self):
        return (self.radka, self.sloupec)

    def na_alg(self) -> str:
        return f"{SLOUPCE[self.sloupec]}{RADKY[self.radka]}"

    @staticmethod
    def z_alg(text: str) -> "Pozice":
        text = text.strip().lower()
        if len(text) != 2 or text[0] not in SLOUPCE or text[1] not in "12345678":
            raise ValueError(f"Neplatne pole: {text!r}")
        return Pozice(RADKY.index(text[1]), SLOUPCE.index(text[0]))

    def na_desce(self) -> bool:
        return 0 <= self.radka < 8 and 0 <= self.sloupec < 8

    def __eq__(self, other) -> bool:
        return isinstance(other, Pozice) and self.to_tuple() == other.to_tuple()

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __repr__(self) -> str:
        return f"Pozice({self.radka}, {self.sloupec})"