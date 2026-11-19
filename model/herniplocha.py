class HerniPlocha:
    def __init__(self, x, y, herni_deska, vyhozene_figurky_b, vyhozene_figurky_c):
        self.x = x
        self.y = y
        self.herni_deska = herni_deska #why?
        self.vyhozene_figurky_b = vyhozene_figurky_b
        self.vyhozene_figurky_c = vyhozene_figurky_c

    def get_coord(self): #use this to check if squere is occupied
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)