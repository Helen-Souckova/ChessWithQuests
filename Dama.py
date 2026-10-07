from Figurka import Figurka


class Dama(Figurka):
    def __init__(self, barva: int):
        super().__init__(barva, "Dama")

        self.vektory = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]
        self.vektory_utoku = self.vektory
        self.skok = False

    def muze_se_pohnout(self, plocha, start, cil):
        dr = cil[0] - start[0]
        dc = cil[1] - start[1]

        if not (
            dr == 0
            or dc == 0
            or abs(dr) == abs(dc)
        ):
            return False

        return plocha.cesta_volna(start, cil)