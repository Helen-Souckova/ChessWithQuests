
class Uzivatel:
    def __init__(self, uzivatelske_jmeno, jmeno, email, heslo):
        self.uzivatelske_jmeno = uzivatelske_jmeno
        self.jmeno = jmeno
        self.email = email
        self.heslo = heslo

class Quest:
    def __init__(self, nazev, popis):
        self.nazev = nazev
        self.popis = popis

class Hrac:
    def __init__(self, barva, uzivatel):
        self.barva = barva
        self.uzivatel = uzivatel

class GameManager:
    def __init__(self, plocha, aktivni_hrac, hraci, aktualni_tah, casovac, game_logger, revizor_tahu):
        self.plocha = HerniPlocha
        self.aktivni_hrac = aktivni_hrac
        self.hraci = Hrac
        self.aktualni_tah = Tah
        self.casovac = Timer
        self.game_logger = GameLogger
        self.revizor_tahu = RevizorTahu

class Timer:
    def __init__(self, cas_hrac):
        self.cas_hrac = cas_hrac

class Gamelogger:
    def __init__(self, soubor):
        self.soubor = soubor

class RevizorTahu:
    def __init__(self, herni_plocha, tah):
        self.herni_plocha = HerniPlocha
        self.tah = Tah

class Tah:
    def __init__(self, vychozi_pozice, cilova_pozice, figurka, typ_tahu):
        self.vychozi_pozice = vychozi_pozice
        self.cilova_pozice = cilova_pozice
        self.figurka = Figurka
        self.typ_tahu = typ_tahu

class HerniPlocha:
    def __init__(self, rozmery, herni_deska, vyhozene_figurky_b, vyhozene_figurky_c):
        self.rozmery = rozmery
        self.herni_deska = herni_deska
        self.vyhozene_figurky_b = vyhozene_figurky_b
        self.vyhozene_figurky_c = vyhozene_figurky_c

class GameLogger:
    def __init__(self, soubor):
        self.soubor = soubor
    
class Figurka:
    def __init__(self, nazev, vektory_utoku, barva, vektory, skok):
        self.nazev = nazev
        self.vektory_utoku = vektory_utoku
        self.barva = barva
        self.vektory = vektory
        self.skok = skok

class Kun(Figurka):
    pass

#dont be stupid and create classes seperatly, this is stupid
