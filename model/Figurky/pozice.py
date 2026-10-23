#EXPERIMENTAL
#pozice will get updated if jmeno_figurky.update_pozice(souradnice pozice)
class Pozice:
    def __init__(self, pozice):
        self.pozice = pozice

    def update_pozice(self, new_pozice):
        self.pozice = new_pozice