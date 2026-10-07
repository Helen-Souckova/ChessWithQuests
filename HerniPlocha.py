
class HerniPlocha:

    def __init__(self):
        self.rozmery = (8, 8)

        self.herni_deska: list[list[Optional[Figurka]]] = [
            [None for _ in range(8)]
            for _ in range(8)
        ]

        self.vyhozene_figurky_b: list[Figurka] = []
        self.vyhozene_figurky_c: list[Figurka] = []

        self.vytvor_pocatecni_postaveni()

    def vrat_obsah(self, souradnice):
        r, c = souradnice

        if not self.je_v_rozsahu(souradnice):
            return None

        return self.herni_deska[r][c]

    def je_v_rozsahu(self, souradnice):
        r, c = souradnice

        return (
            0 <= r < 8
            and 0 <= c < 8
        )

    def cesta_volna(self, start, cil):

        dr = cil[0] - start[0]
        dc = cil[1] - start[1]

        krok_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        krok_c = 0 if dc == 0 else (1 if dc > 0 else -1)

        r = start[0] + krok_r
        c = start[1] + krok_c

        while (r, c) != cil:

            if self.herni_deska[r][c] is not None:
                return False

            r += krok_r
            c += krok_c

        return True

    def posun_figurky(self, tah: Tah) -> bool:

        start = tah.vychozi_pozice
        cil = tah.cilova_pozice

        figurka = self.vrat_obsah(start)

        if figurka is None:
            return False

        cilova_figurka = self.vrat_obsah(cil)

        # Vyhození soupeřovy figurky.
        if cilova_figurka is not None:

            if cilova_figurka.barva == 1:
                self.vyhozene_figurky_b.append(cilova_figurka)
            else:
                self.vyhozene_figurky_c.append(cilova_figurka)

        self.herni_deska[cil[0]][cil[1]] = figurka
        self.herni_deska[start[0]][start[1]] = None

        # Proměna pěšce na dámu.
        if isinstance(figurka, Pesec):
            if figurka.barva == 1 and cil[0] == 0:
                self.herni_deska[cil[0]][cil[1]] = Dama(figurka.barva)

            elif figurka.barva == -1 and cil[0] == 7:
                self.herni_deska[cil[0]][cil[1]] = Dama(figurka.barva)

        return True

    def nahrad_figurku(self, figurka, tah):
        self.herni_deska[
            tah.cilova_pozice[0]
        ][
            tah.cilova_pozice[1]
        ] = figurka

    def vytvor_pocatecni_postaveni(self):

        # Černé figurky nahoře.
        zadni_cerna = [
            Vez(-1),
            Kun(-1),
            Strelec(-1),
            Dama(-1),
            Kral(-1),
            Strelec(-1),
            Kun(-1),
            Vez(-1)
        ]

        for col, figurka in enumerate(zadni_cerna):
            self.herni_deska[0][col] = figurka
            self.herni_deska[1][col] = Pesec(-1)

        # Bílé figurky dole.
        zadni_bila = [
            Vez(1),
            Kun(1),
            Strelec(1),
            Dama(1),
            Kral(1),
            Strelec(1),
            Kun(1),
            Vez(1)
        ]

        for col, figurka in enumerate(zadni_bila):
            self.herni_deska[7][col] = figurka
            self.herni_deska[6][col] = Pesec(1)
