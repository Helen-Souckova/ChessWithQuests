from Game_core.figurka import Figurka
from Game_core.pozice import Pozice
from core import TYP_NORMAL
from typing import Optional


class Tah:
    """Jeden tah vcetne typu (brani, rosada, en passant, promena)."""

    def __init__(self, vychozi_pozice: Pozice, cilova_pozice: Pozice, figurka: Figurka,
                 typ: str = TYP_NORMAL, figurka_brana: Optional[Figurka] = None,
                 povyseni: Optional[type] = None):
        self.vychozi_pozice = vychozi_pozice
        self.cilova_pozice = cilova_pozice
        self.figurka = figurka
        self.typ = typ
        self.figurka_brana = figurka_brana
        self.povyseni = povyseni
        self.nova_figurka: Optional[Figurka] = None
        self.sach = False
        self.mat = False
        self.notation = ""

    @property
    def je_brani(self) -> bool:
        return self.figurka_brana is not None

    def __str__(self) -> str:
        text = f"{self.vychozi_pozice.na_alg()}{self.cilova_pozice.na_alg()}"
        if self.povyseni is not None:
            text += self.povyseni.zkratka.lower()
        return text