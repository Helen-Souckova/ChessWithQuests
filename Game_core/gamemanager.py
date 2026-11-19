from Figurky.kral import Kral
from Figurky.pesak import Pesak
from Game_core.gamelogger import GameLogger
from Game_core.herniplocha import HerniPlocha
from Game_core.hrac import Hrac
from Game_core.revizortahu import RevizorTahu
from Game_core.tah import Tah
from Game_core.uzivatel import Uzivatel
from core import CERNY, BILY, nazev_barvy, TYP_MALA_ROCHADA, TYP_VELKA_ROCHADA, SLOUPCE, RADKY
from typing import List
from Game_core.timer import Timer
class GameManager:
    """Ridi hru: stridani hracu, kontrola konce, notace."""

    def __init__(self, cas_na_hru: int = 300):
        self.plocha = HerniPlocha()
        self.revizor = RevizorTahu(self.plocha)
        self.casovac = Timer(cas_na_hru)
        self.game_logger = GameLogger()
        self.aktivni_hrac = BILY
        self.hraci = [
            Hrac(BILY, Uzivatel("bily", "Bily hrac", "bily@example.com")),
            Hrac(CERNY, Uzivatel("cerny", "Cerny hrac", "cerny@example.com")),
        ]
        self.historie: List[Tah] = []
        self.konec = False
        self.vysledek = ""

    def hrac(self, barva: int) -> Hrac:
        return self.hraci[barva]

    def proved_tah(self, tah: Tah) -> bool:
        if self.konec:
            return False
        tah.notation = self._notace(tah)
        self.plocha.posun_figurky(tah)
        self.historie.append(tah)
        self.game_logger.uloz_tah(tah)
        self.casovac.prepni(self.aktivni_hrac)
        self.aktivni_hrac = 1 - self.aktivni_hrac
        self._vyhodnot_stav(tah)
        return True

    def vzdat(self) -> None:
        if self.konec:
            return
        self.konec = True
        self.vysledek = (f"Hrac {nazev_barvy(self.aktivni_hrac)} se vzdal, "
                         f"vyhral {nazev_barvy(1 - self.aktivni_hrac)}.")

    def cas_v_poradku(self) -> bool:
        if self.konec:
            return False
        if self.casovac.vyprsel(self.aktivni_hrac):
            self.konec = True
            self.vysledek = (f"Hrac {nazev_barvy(self.aktivni_hrac)} prekrocil cas, "
                             f"vyhral {nazev_barvy(1 - self.aktivni_hrac)}.")
            return False
        return True

    # ---------- interni ----------

    def _vyhodnot_stav(self, tah: Tah) -> None:
        na_tahu = self.aktivni_hrac
        tah.sach = self.revizor.check_sach(na_tahu)
        tahy = self.revizor.vsechny_legalni_tahy(na_tahu)
        if not tahy:
            self.konec = True
            if tah.sach:
                tah.mat = True
                self.vysledek = f"Mat! Vyhral {nazev_barvy(1 - na_tahu)}."
            else:
                self.vysledek = "Pat - remiza."
        tah.notation += "#" if tah.mat else ("+" if tah.sach else "")

    def _notace(self, tah: Tah) -> str:
        if tah.typ == TYP_MALA_ROCHADA:
            return "0-0"
        if tah.typ == TYP_VELKA_ROCHADA:
            return "0-0-0"

        figurka = tah.figurka
        cil = tah.cilova_pozice.na_alg()
        if isinstance(figurka, Pesak):
            zaklad = cil
            if tah.figurka_brana is not None:
                zaklad = f"{SLOUPCE[tah.vychozi_pozice.sloupec]}x{cil}"
        else:
            brani = "x" if tah.figurka_brana is not None else ""
            zaklad = f"{figurka.zkratka}{self._disambiguace(tah)}{brani}{cil}"
        if tah.povyseni is not None:
            zaklad += f"={tah.povyseni.zkratka}"
        return zaklad

    def _disambiguace(self, tah: Tah) -> str:
        figurka = tah.figurka
        if isinstance(figurka, (Pesak, Kral)):
            return ""
        kolize = []
        for druha in self.plocha.vsechny_figurky(figurka.barva):
            if druha is figurka or type(druha) is not type(figurka):
                continue
            for tah_druhe in self.revizor.get_legalni_tahy(druha):
                if tah_druhe.cilova_pozice == tah.cilova_pozice:
                    kolize.append(druha)
                    break
        if not kolize:
            return ""
        if all(k.sloupec != figurka.pozice.sloupec for k in kolize):
            return SLOUPCE[figurka.pozice.sloupec]
        if all(k.radka != figurka.pozice.radka for k in kolize):
            return RADKY[figurka.pozice.radka]
        return figurka.pozice.na_alg()