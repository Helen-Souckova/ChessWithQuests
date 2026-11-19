from model import hrac, timer, tah
from model.herniplocha import HerniPlocha
from model.revizortahu import RevizorTahu


class GameManager:
    def __init__(self, plocha, aktivni_hrac, hraci, aktualni_tah, casovac, game_logger, revizor_tahu):
        self.plocha = HerniPlocha
        self.aktivni_hrac = aktivni_hrac
        self.hraci = hrac
        self.aktualni_tah = tah
        self.casovac = timer
        self.revizor_tahu = RevizorTahu

#i have no idea what anz of it is supposed to do