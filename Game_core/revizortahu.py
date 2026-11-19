from Figurky.dama import Dama
from Figurky.kral import Kral
from Figurky.kun import Kun
from Figurky.pesak import Pesak
from Figurky.strelec import Strelec
from Figurky.vez import Vez
from Game_core.figurka import Figurka
from Game_core.herniplocha import HerniPlocha
from Game_core.pozice import Pozice

from typing import List, Optional

from Game_core.tah import Tah
from core import TYP_BRANI, TYP_NORMAL, TYP_EN_PASSANT, BILY, TYP_PROMOCE, TYP_MALA_ROCHADA, TYP_VELKA_ROCHADA


class RevizorTahu:


    def __init__(self, herni_plocha: HerniPlocha):
        self.herni_plocha = herni_plocha

    # ---------- nápady (utoky) ----------

    def muze_ohrozit(self, figurka: Figurka, cil: Pozice) -> bool:
        d_radka = cil.radka - figurka.pozice.radka
        d_sloupec = cil.sloupec - figurka.pozice.sloupec

        if d_radka == 0 and d_sloupec == 0:
            return False

        if isinstance(figurka, Kun):
            return (abs(d_radka), abs(d_sloupec)) in ((1, 2), (2, 1))
        if isinstance(figurka, Kral):
            return max(abs(d_radka), abs(d_sloupec)) == 1
        if isinstance(figurka, Pesak):
            return d_radka == figurka.smer and abs(d_sloupec) == 1

        diagonala = abs(d_radka) == abs(d_sloupec)
        primka = d_radka == 0 or d_sloupec == 0

        if isinstance(figurka, Strelec) and not diagonala:
            return False
        if isinstance(figurka, Vez) and not primka:
            return False
        if isinstance(figurka, Dama) and not (diagonala or primka):
            return False
        if not isinstance(figurka, (Strelec, Vez, Dama)):
            return False

        krok_r = (d_radka > 0) - (d_radka < 0)
        krok_s = (d_sloupec > 0) - (d_sloupec < 0)
        radka = figurka.pozice.radka + krok_r
        sloupec = figurka.pozice.sloupec + krok_s
        while (radka, sloupec) != (cil.radka, cil.sloupec):
            if self.herni_plocha.herni_deska[radka][sloupec] is not None:
                return False
            radka += krok_r
            sloupec += krok_s
        return True

    def je_napadnute(self, pozice: Pozice, barva_utocnika: int) -> bool:
        for figurka in self.herni_plocha.vsechny_figurky(barva_utocnika):
            if self.muze_ohrozit(figurka, pozice):
                return True
        return False

    def check_sach(self, barva: int) -> bool:
        kral = self.herni_plocha.najdi_krale(barva)
        if kral is None:
            return False
        return self.je_napadnute(kral.pozice, 1 - barva)

    # ---------- generovani tahu ----------

    def get_mozne_tahy(self, figurka: Figurka) -> List[Tah]:
        """Tahy podle pohybu figurky, bez ohledu na vlastniho krale."""
        if isinstance(figurka, Pesak):
            tahy = self._tahy_pesaka(figurka)
        else:
            tahy = []
            for radka in range(8):
                for sloupec in range(8):
                    cil = Pozice(radka, sloupec)
                    obsah = self.herni_plocha.vrat_obsah(cil)
                    if obsah is not None and obsah.barva == figurka.barva:
                        continue
                    if self.muze_ohrozit(figurka, cil):
                        typ = TYP_BRANI if obsah is not None else TYP_NORMAL
                        tahy.append(Tah(figurka.pozice, cil, figurka, typ, obsah))
        if isinstance(figurka, Kral):
            tahy.extend(self._rochady(figurka))
        return tahy

    def get_legalni_tahy(self, figurka: Figurka) -> List[Tah]:
        """Tahy, po kterych vlastni kral nezustane v sachu."""
        legalni = []
        for tah in self.get_mozne_tahy(figurka):
            kopie = self.herni_plocha.po_tahu(tah)
            if not RevizorTahu(kopie).check_sach(figurka.barva):
                legalni.append(tah)
        return legalni

    def vsechny_legalni_tahy(self, barva: int) -> List[Tah]:
        tahy = []
        for figurka in self.herni_plocha.vsechny_figurky(barva):
            tahy.extend(self.get_legalni_tahy(figurka))
        return tahy

    # ---------- pomocne ----------

    def _tahy_pesaka(self, pesak: Pesak) -> List[Tah]:
        tahy: List[Tah] = []
        radka = pesak.pozice.radka
        sloupec = pesak.pozice.sloupec
        cil_radka = radka + pesak.smer
        if not 0 <= cil_radka < 8:
            return tahy

        if self.herni_plocha.vrat_obsah(Pozice(cil_radka, sloupec)) is None:
            tahy.extend(self._tah_pesaka(pesak, Pozice(cil_radka, sloupec), None))
            if radka == pesak.vychozi_radka:
                dvojity = radka + 2 * pesak.smer
                if self.herni_plocha.vrat_obsah(Pozice(dvojity, sloupec)) is None:
                    tahy.append(Tah(pesak.pozice, Pozice(dvojity, sloupec), pesak))

        for posun in (-1, 1):
            cil_sloupec = sloupec + posun
            if not 0 <= cil_sloupec < 8:
                continue
            cil = Pozice(cil_radka, cil_sloupec)
            obsah = self.herni_plocha.vrat_obsah(cil)
            if obsah is not None and obsah.barva != pesak.barva:
                tahy.extend(self._tah_pesaka(pesak, cil, obsah))
            elif obsah is None and self.herni_plocha.en_passant == cil:
                obet = self.herni_plocha.vrat_obsah(Pozice(radka, cil_sloupec))
                if obet is not None and obet.barva != pesak.barva:
                    tahy.append(Tah(pesak.pozice, cil, pesak, TYP_EN_PASSANT, obet))
        return tahy

    def _tah_pesaka(self, pesak: Pesak, cil: Pozice, brana: Optional[Figurka]) -> List[Tah]:
        posledni_radka = 0 if pesak.barva == BILY else 7
        if cil.radka == posledni_radka:
            return [Tah(pesak.pozice, cil, pesak, TYP_PROMOCE, brana, trida)
                    for trida in (Dama, Vez, Strelec, Kun)]
        typ = TYP_BRANI if brana is not None else TYP_NORMAL
        return [Tah(pesak.pozice, cil, pesak, typ, brana)]

    def _rochady(self, kral: Kral) -> List[Tah]:
        tahy: List[Tah] = []
        if kral.pocet_tahu != 0:
            return tahy
        radka = 7 if kral.barva == BILY else 0
        if kral.pozice.radka != radka or kral.pozice.sloupec != 4:
            return tahy
        if self.check_sach(kral.barva):
            return tahy

        souper = 1 - kral.barva
        vez = self.herni_plocha.vrat_obsah(Pozice(radka, 7))
        if (isinstance(vez, Vez) and vez.barva == kral.barva and vez.pocet_tahu == 0
                and self.herni_plocha.vrat_obsah(Pozice(radka, 5)) is None
                and self.herni_plocha.vrat_obsah(Pozice(radka, 6)) is None
                and not self.je_napadnute(Pozice(radka, 5), souper)
                and not self.je_napadnute(Pozice(radka, 6), souper)):
            tahy.append(Tah(kral.pozice, Pozice(radka, 6), kral, TYP_MALA_ROCHADA))

        vez = self.herni_plocha.vrat_obsah(Pozice(radka, 0))
        if (isinstance(vez, Vez) and vez.barva == kral.barva and vez.pocet_tahu == 0
                and self.herni_plocha.vrat_obsah(Pozice(radka, 1)) is None
                and self.herni_plocha.vrat_obsah(Pozice(radka, 2)) is None
                and self.herni_plocha.vrat_obsah(Pozice(radka, 3)) is None
                and not self.je_napadnute(Pozice(radka, 3), souper)
                and not self.je_napadnute(Pozice(radka, 2), souper)):
            tahy.append(Tah(kral.pozice, Pozice(radka, 2), kral, TYP_VELKA_ROCHADA))
        return tahy