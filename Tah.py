@dataclass
class Tah:
    vychozi_pozice: tuple[int, int]
    cilova_pozice: tuple[int, int]
    figurka: "Figurka"
    typ_tahu: str = "normalni"

    def over_platnost(self, plocha: "HerniPlocha") -> bool:
        return self.figurka.je_platny_tah(
            plocha,
            self.vychozi_pozice,
            self.cilova_pozice
        )

    def proved_tah(self, plocha: "HerniPlocha"):
        plocha.posun_figurky(self)
