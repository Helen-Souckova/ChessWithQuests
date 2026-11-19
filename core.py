

from __future__ import annotations

import copy
import sys
import time
from typing import List, Optional

from Figurky.dama import Dama
from Figurky.kun import Kun
from Figurky.strelec import Strelec
from Figurky.vez import Vez
from Game_core.figurka import Figurka
from Game_core.gamemanager import GameManager
from Game_core.pozice import Pozice
from Game_core.tah import Tah

SLOUPCE = "abcdefgh"
RADKY = "87654321"

BILY = 0
CERNY = 1

TYP_NORMAL = "normal"
TYP_BRANI = "brani"
TYP_MALA_ROCHADA = "mala_rochada"
TYP_VELKA_ROCHADA = "velka_rochada"
TYP_EN_PASSANT = "en_passant"
TYP_PROMOCE = "promoce"


def nazev_barvy(barva: int) -> str:
    return "bily" if barva == BILY else "cerny"


def format_casu(sekundy: float) -> str:
    celkem = max(0, int(sekundy))
    return f"{celkem // 60:02d}:{celkem % 60:02d}"


# ==================================================================
# 2. VIEW + CONTROLLER - konzolove rozhrani (nahrazuje tkinter)
# ==================================================================

class KonzoloveRozhrani:
    def __init__(self, hra: GameManager):
        self.hra = hra

    def uvod(self) -> None:
        print("=" * 46)
        print("  SACHY - konzolova verze (bez GUI)")
        print("=" * 46)
        print("  Tah zadejte jako e2e4, seznam prikazu: tahy")
        print("  Prikazy: tahy, deska, historie, uloz, vzdat, konec")
        print("=" * 46)

    def vykresli(self) -> None:
        plocha = self.hra.plocha
        bile = self.hra.hrac(BILY)
        cerne = self.hra.hrac(CERNY)

        print()
        print(f"  {cerne.uzivatel.jmeno} ({cerne.getEloRating()} ELO)   "
              f"{format_casu(self.hra.casovac.zbyva(CERNY))}"
              + ("   <- na tahu" if self.hra.aktivni_hrac == CERNY else ""))
        print("    " + "  ".join(SLOUPCE))
        print("  +" + "-" * 24 + "+")
        for radka in range(8):
            bunky = []
            for sloupec in range(8):
                figurka = plocha.herni_deska[radka][sloupec]
                bunky.append(figurka.symbol if figurka is not None else ".")
            print(f"{RADKY[radka]} |" + "".join(f" {b} " for b in bunky) + "|")
        print("  +" + "-" * 24 + "+")
        print("    " + "  ".join(SLOUPCE))
        print(f"  {bile.uzivatel.jmeno} ({bile.getEloRating()} ELO)   "
              f"{format_casu(self.hra.casovac.zbyva(BILY))}"
              + ("   <- na tahu" if self.hra.aktivni_hrac == BILY else ""))
        if self.hra.revizor.check_sach(self.hra.aktivni_hrac):
            print("  SACH!")

    def vypis_legalni_tahy(self, figurka: Optional[Figurka] = None) -> None:
        if figurka is None:
            tahy = self.hra.revizor.vsechny_legalni_tahy(self.hra.aktivni_hrac)
        else:
            tahy = self.hra.revizor.get_legalni_tahy(figurka)
        if not tahy:
            print("  (zadny legalni tah)")
            return
        print("  " + "  ".join(sorted(str(t) for t in tahy)))

    def vypis_historie(self) -> None:
        if not self.hra.historie:
            print("  Zatim zadne tahy.")
            return
        tahy = self.hra.historie
        for index in range(0, len(tahy), 2):
            cislo = index // 2 + 1
            bily = tahy[index].notation
            cerny = tahy[index + 1].notation if index + 1 < len(tahy) else ""
            print(f"  {cislo:>3}. {bily:<8} {cerny}")

    def parsuj_tah(self, vstup: str) -> Optional[Tah]:
        text = vstup.replace(" ", "").replace("-", "").replace("x", "")
        if len(text) < 4:
            print("  ! Tah zadejte jako e2e4 (promena treba e7e8d).")
            return None
        try:
            start = Pozice.z_alg(text[0:2])
            cil = Pozice.z_alg(text[2:4])
        except ValueError:
            print("  ! Neplatny zapis pole, pouzijte napr. e2e4.")
            return None

        povyseni = None
        if len(text) >= 5:
            mapa = {"d": Dama, "v": Vez, "s": Strelec, "j": Kun}
            povyseni = mapa.get(text[4])
            if povyseni is None:
                print("  ! Neznamy typ promeny (d, v, s, j).")
                return None

        figurka = self.hra.plocha.vrat_obsah(start)
        if figurka is None:
            print("  ! Na tomto poli neni zadna figurka.")
            return None
        if figurka.barva != self.hra.aktivni_hrac:
            print("  ! Tato figurka neni vase.")
            return None

        kandidati = [t for t in self.hra.revizor.get_legalni_tahy(figurka)
                     if t.cilova_pozice == cil]
        if not kandidati:
            print("  ! Tento tah neni mozny.")
            self.vypis_legalni_tahy(figurka)
            return None
        if len(kandidati) > 1:
            promeny = [t for t in kandidati if t.povyseni is not None]
            if promeny:
                if povyseni is None:
                    print("  i Bez zadane promeny povysuji na damu.")
                return next((t for t in promeny if t.povyseni is povyseni), promeny[0])
        return kandidati[0]

    def hraj(self) -> None:
        self.uvod()
        while not self.hra.konec:
            self.vykresli()
            if not self.hra.cas_v_poradku():
                break
            try:
                prikaz = input(f"  {nazev_barvy(self.hra.aktivni_hrac)} na tahu > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                print("  Hra ukoncena.")
                return
            if not prikaz:
                continue
            if prikaz in ("konec", "quit", "q", "exit"):
                print("  Hra ukoncena.")
                return
            if prikaz in ("vzdat", "resign"):
                self.hra.vzdat()
                break
            if prikaz in ("tahy", "pomoc", "help"):
                self.vypis_legalni_tahy()
                continue
            if prikaz in ("deska", "board"):
                continue
            if prikaz in ("historie", "history"):
                self.vypis_historie()
                continue
            if prikaz in ("uloz", "save"):
                cesta = self.hra.game_logger.uloz_do_souboru()
                print(f"  Partie ulozena do {cesta}")
                continue
            tah = self.parsuj_tah(prikaz)
            if tah is None:
                continue
            self.hra.proved_tah(tah)
            print(f"  Odehrano: {tah.notation}")

        self.vykresli()
        print()
        print("  " + self.hra.vysledek)


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    hra = GameManager()
    KonzoloveRozhrani(hra).hraj()


if __name__ == "__main__":
    main()
