class Figurka(ABC):

    SYMBOLY = {
        (1, "Kral"): "♔",
        (1, "Dama"): "♕",
        (1, "Vez"): "♖",
        (1, "Strelec"): "♗",
        (1, "Kun"): "♘",
        (1, "Pesec"): "♙",

        (-1, "Kral"): "♚",
        (-1, "Dama"): "♛",
        (-1, "Vez"): "♜",
        (-1, "Strelec"): "♝",
        (-1, "Kun"): "♞",
        (-1, "Pesec"): "♟",
    }

    def __init__(self, barva: int, nazev: str):
        self.nazev = nazev
        self.barva = barva

        # V diagramu jsou vektory a vektory_utoku
        self.vektory = []
        self.vektory_utoku = []

    @property
    def symbol(self):
        return self.SYMBOLY[(self.barva, self.nazev)]

    @abstractmethod
    def muze_se_pohnout(
        self,
        plocha: "HerniPlocha",
        start: tuple[int, int],
        cil: tuple[int, int]
    ) -> bool:
        pass

    def je_platny_tah(
        self,
        plocha: "HerniPlocha",
        start: tuple[int, int],
        cil: tuple[int, int]
    ) -> bool:

        if not plocha.je_v_rozsahu(cil):
            return False

        cilova_figurka = plocha.vrat_obsah(cil)

        # Nesmíme sebrat vlastní figurku.
        if cilova_figurka and cilova_figurka.barva == self.barva:
            return False

        return self.muze_se_pohnout(plocha, start, cil)