class Pesec(Figurka):
    def __init__(self, barva: int):
        super().__init__(barva, "Pesec")

        self.vektory = [
            (1, 0)
        ]

        self.vektory_utoku = [
            (1, -1),
            (1, 1)
        ]

        self.skok = False

    def muze_se_pohnout(self, plocha, start, cil):

        smer = self.barva

        dr = cil[0] - start[0]
        dc = cil[1] - start[1]

        cilova_figurka = plocha.vrat_obsah(cil)

        # Normální pohyb o jedno pole.
        if dc == 0 and dr == smer and cilova_figurka is None:
            return True

        # První pohyb o dvě pole.
        startovni_radek = 6 if self.barva == 1 else 1

        if (
            dc == 0
            and dr == 2 * smer
            and start[0] == startovni_radek
            and cilova_figurka is None
        ):
            mez = (start[0] + smer, start[1])

            if plocha.vrat_obsah(mez) is None:
                return True

        # Braní šikmo.
        if abs(dc) == 1 and dr == smer:
            return cilova_figurka is not None and \
                   cilova_figurka.barva != self.barva

        return False