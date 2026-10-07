class Kun(Figurka):
    def __init__(self, barva: int):
        super().__init__(barva, "Kun")

        # Podle diagramu je u koně skok=True.
        self.vektory = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]
        self.vektory_utoku = self.vektory
        self.skok = True

    def muze_se_pohnout(self, plocha, start, cil):
        dr = cil[0] - start[0]
        dc = cil[1] - start[1]

        return (dr, dc) in self.vektory
