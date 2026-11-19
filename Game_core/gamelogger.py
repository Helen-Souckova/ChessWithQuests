from Game_core.tah import Tah
from typing import List

class GameLogger:
    """Zaznam partie v algebraicke notaci."""

    def __init__(self, soubor: str = "partie.txt"):
        self.soubor = soubor
        self.zaznamy: List[Tah] = []

    def uloz_tah(self, tah: Tah) -> None:
        self.zaznamy.append(tah)

    def text(self) -> str:
        radky = []
        for index in range(0, len(self.zaznamy), 2):
            cislo = index // 2 + 1
            bily = self.zaznamy[index].notation
            cerny = self.zaznamy[index + 1].notation if index + 1 < len(self.zaznamy) else ""
            radky.append(f"{cislo}. {bily} {cerny}".rstrip())
        return "\n".join(radky)

    #def uloz_do_souboru(self, cesta: Optional[str] = None) -> str:
        cesta = cesta or self.soubor
        with open(cesta, "w", encoding="utf-8") as soubor:
            soubor.write(self.text() + "\n")
        return cesta