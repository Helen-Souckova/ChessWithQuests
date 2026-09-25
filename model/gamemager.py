class GameManager:
    def __init__(self, plocha, aktivni_hrac, hraci, aktualni_tah, casovac, game_logger, revizor_tahu):
        self.plocha = HerniPlocha
        self.aktivni_hrac = aktivni_hrac
        self.hraci = Hrac
        self.aktualni_tah = Tah
        self.casovac = Timer
        self.game_logger = GameLogger
        self.revizor_tahu = RevizorTahu