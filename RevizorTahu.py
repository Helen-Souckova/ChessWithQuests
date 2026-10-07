class RevizorTahu:

    def je_platny(self, plocha: HerniPlocha, tah: Tah) -> bool:

        figurka = plocha.vrat_obsah(tah.vychozi_pozice)

        if figurka is None:
            return False

        if figurka.barva != tah.figurka.barva:
            return False

        return tah.over_platnost(plocha)