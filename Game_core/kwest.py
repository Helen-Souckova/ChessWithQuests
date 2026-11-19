class Kwest:
    """Volitelny ukol hrace - z puvodniho modelu."""

    def __init__(self, nazev: str, popis: str, odmena_xp: int = 100):
        self.nazev = nazev
        self.popis = popis
        self.odmena_xp = odmena_xp
        self.splneno = False

    def spln(self) -> None:
        self.splneno = True