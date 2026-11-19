import copy
from typing import List, Optional

from Figurky.dama import Dama
from Figurky.kral import Kral
from Figurky.kun import Kun
from Figurky.pesak import Pesak
from Figurky.strelec import Strelec
from Figurky.vez import Vez
from Game_core.figurka import Figurka
from Game_core.pozice import Pozice
from Game_core.tah import Tah
from core import CERNY, BILY, TYP_EN_PASSANT, TYP_MALA_ROCHADA, TYP_VELKA_ROCHADA, TYP_PROMOCE


class HerniPlocha:
    """Stav sachovnice - 8x8 poli, brané figurky a pole pro en passant."""

    def __init__(self):
        self.rozmery = (8, 8)
        self.herni_deska: List[List[Optional[Figurka]]] = [[None] * 8 for _ in range(8)]
        self.vyhozene_figurky_b: List[Figurka] = []
        self.vyhozene_figurky_c: List[Figurka] = []
        self.en_passant: Optional[Pozice] = None
        self.nastav_zakladni_rozestaveni()

    def nastav_zakladni_rozestaveni(self) -> None:
        poradi = [Vez, Kun, Strelec, Dama, Kral, Strelec, Kun, Vez]
        for sloupec in range(8):
            self.herni_deska[0][sloupec] = poradi[sloupec](CERNY, Pozice(0, sloupec))
            self.herni_deska[1][sloupec] = Pesak(CERNY, Pozice(1, sloupec))
            self.herni_deska[6][sloupec] = Pesak(BILY, Pozice(6, sloupec))
            self.herni_deska[7][sloupec] = poradi[sloupec](BILY, Pozice(7, sloupec))

    def vrat_obsah(self, pozice: Pozice) -> Optional[Figurka]:
        if not pozice.na_desce():
            return None
        return self.herni_deska[pozice.radka][pozice.sloupec]

    def vsechny_figurky(self, barva: int) -> List[Figurka]:
        return [f for radek in self.herni_deska for f in radek
                if f is not None and f.barva == barva]

    def najdi_krale(self, barva: int) -> Optional[Figurka]:
        for figurka in self.vsechny_figurky(barva):
            if isinstance(figurka, Kral):
                return figurka
        return None

    def odeber(self, figurka: Figurka) -> None:
        self.herni_deska[figurka.pozice.radka][figurka.pozice.sloupec] = None
        figurka.aktivni = False
        if figurka.barva == BILY:
            self.vyhozene_figurky_b.append(figurka)
        else:
            self.vyhozene_figurky_c.append(figurka)

    def posun_figurky(self, tah: Tah) -> None:
        figurka = tah.figurka
        start = tah.vychozi_pozice
        cil = tah.cilova_pozice

        # 1) odstraneni brané figurky
        if tah.typ == TYP_EN_PASSANT:
            if tah.figurka_brana is not None:
                self.odeber(tah.figurka_brana)
        elif tah.figurka_brana is not None:
            self.odeber(tah.figurka_brana)

        # 2) presun figurky
        self.herni_deska[start.radka][start.sloupec] = None
        figurka.pozice = cil
        figurka.pocet_tahu += 1
        self.herni_deska[cil.radka][cil.sloupec] = figurka

        # 3) rosada - soucasne presun veze
        if tah.typ == TYP_MALA_ROCHADA:
            vez = self.herni_deska[start.radka][7]
            self.herni_deska[start.radka][7] = None
            vez.pozice = Pozice(start.radka, 5)
            vez.pocet_tahu += 1
            self.herni_deska[start.radka][5] = vez
        elif tah.typ == TYP_VELKA_ROCHADA:
            vez = self.herni_deska[start.radka][0]
            self.herni_deska[start.radka][0] = None
            vez.pozice = Pozice(start.radka, 3)
            vez.pocet_tahu += 1
            self.herni_deska[start.radka][3] = vez

        # 4) promena pesaka
        if tah.typ == TYP_PROMOCE and tah.povyseni is not None:
            nova = tah.povyseni(figurka.barva, cil)
            nova.pocet_tahu = figurka.pocet_tahu
            figurka.aktivni = False
            self.herni_deska[cil.radka][cil.sloupec] = nova
            tah.nova_figurka = nova

        # 5) nove pole pro en passant
        self.en_passant = None
        if isinstance(figurka, Pesak) and abs(cil.radka - start.radka) == 2:
            self.en_passant = Pozice((cil.radka + start.radka) // 2, cil.sloupec)

    def po_tahu(self, tah: Tah) -> "HerniPlocha":
        """Vrati kopii plochy po provedeni tahu (puvodni plocha zustava nedotcena)."""
        kopie = copy.deepcopy(self)
        figurka = kopie.vrat_obsah(tah.vychozi_pozice)
        brana = None
        if tah.figurka_brana is not None:
            brana = kopie.vrat_obsah(tah.figurka_brana.pozice)
        novy = Tah(tah.vychozi_pozice, tah.cilova_pozice, figurka, tah.typ, brana, tah.povyseni)
        kopie.posun_figurky(novy)
        return kopie