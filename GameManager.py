class GameManager:

    def __init__(self, hraci: list[Hrac]):

        self.plocha = HerniPlocha()

        self.aktivni_hrac = 1
        self.hraci = hraci

        self.aktualni_tah: Optional[Tah] = None

        self.casovac = Timer(600)
        self.game_logger = GameLogger()
        self.revizor_tahu = RevizorTahu()

        self.historie_tahu = []

        self.hra_bezi = True

    def zacni_tah(self):

        self.aktualni_tah = None
        return True

    def mozne_tahy(self):

        tahy = []

        for r in range(8):
            for c in range(8):

                figurka = self.plocha.vrat_obsah((r, c))

                if figurka is None:
                    continue

                if figurka.barva != self.aktivni_hrac:
                    continue

                for tr in range(8):
                    for tc in range(8):

                        cil = (tr, tc)

                        tah = Tah(
                            (r, c),
                            cil,
                            figurka
                        )

                        if self.revizor_tahu.je_platny(
                            self.plocha,
                            tah
                        ):
                            tahy.append(tah)

        return tahy

    def proved_tah(self, start, cil):

        figurka = self.plocha.vrat_obsah(start)

        if figurka is None:
            return False, "Na výchozím poli není figurka."

        if figurka.barva != self.aktivni_hrac:
            return False, "Tato figurka není na tahu."

        tah = Tah(start, cil, figurka)

        if not self.revizor_tahu.je_platny(
            self.plocha,
            tah
        ):
            return False, "Neplatný tah."

        # Kontrola, zda soupeřův král nebyl sebrán.
        cilova = self.plocha.vrat_obsah(cil)

        if isinstance(cilova, Kral):
            return False, "Krále nelze přímo sebrat. Prototyp zatím používá jednodušší pravidla."

        self.plocha.posun_figurky(tah)

        self.aktualni_tah = tah
        self.historie_tahu.append(tah)

        self.game_logger.uloz(
            f"{self.barva_text(figurka.barva)}: "
            f"{self.souradnice_text(start)} -> "
            f"{self.souradnice_text(cil)}"
        )

        # Přepnutí hráče.
        self.aktivni_hrac *= -1

        return True, "Tah proveden."

    def barva_text(self, barva):
        return "Bílý" if barva == 1 else "Černý"

    def souradnice_text(self, souradnice):
        r, c = souradnice

        pismeno = chr(ord("a") + c)
        cislo = 8 - r

        return f"{pismeno}{cislo}"

    def je_vlastni_figurka(self, souradnice):
        figurka = self.plocha.vrat_obsah(souradnice)

        return (
            figurka is not None
            and figurka.barva == self.aktivni_hrac
        )

    def zrus_tah(self):
        # Jednoduchá možnost vrátit poslední tah.
        if not self.historie_tahu:
            return False

        # Pro jednoduchost vytvoříme novou desku
        # a znovu přehrajeme všechny tahy kromě posledního.
        historie = self.historie_tahu[:-1]

        self.plocha = HerniPlocha()

        for tah in historie:
            figurka = self.plocha.vrat_obsah(tah.vychozi_pozice)

            if figurka is not None:
                novy_tah = Tah(
                    tah.vychozi_pozice,
                    tah.cilova_pozice,
                    figurka
                )

                if self.revizor_tahu.je_platny(
                    self.plocha,
                    novy_tah
                ):
                    self.plocha.posun_figurky(novy_tah)

        self.historie_tahu = historie
        self.aktivni_hrac *= -1

        return True

    def get_stav(self):
        return 1 if self.hra_bezi else 0

    def najdi_uzivatele(self, id):
        if 0 <= id < len(self.hraci):
            return self.hraci[id].uzivatel

        return None

    def uloz_log(self):
        with open("game_log.txt", "w", encoding="utf-8") as soubor:
            for radek in self.game_logger.vrat_log():
                soubor.write(radek + "\n")
