class Vez(Figurka):
    def __init__(self, barva: int):
        super().__init__(barva, "Vez")

        self.vektory = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]
        self.vektory_utoku = self.vektory
        self.skok = False

    def muze_se_pohnout(self, plocha, start, cil):
        dr = cil[0] - start[0]
        dc = cil[1] - start[1]

        if dr != 0 and dc != 0:
            return False

        return plocha.cesta_volna(start, cil)