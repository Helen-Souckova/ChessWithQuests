class Kral(Figurka):
    def __init__(self, barva: int):
        super().__init__(barva, "Kral")

        self.vektory = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        self.vektory_utoku = self.vektory
        self.skok = False

    def muze_se_pohnout(self, plocha, start, cil):
        dr = cil[0] - start[0]
        dc = cil[1] - start[1]

        return max(abs(dr), abs(dc)) == 1
