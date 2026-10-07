class GameManagerController:

    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.herni_plocha = game_manager.plocha
        self.game_view = None
        self.hrac_view = None

    def vyber_pole(self, souradnice):
        return self.game_manager.plocha.vrat_obsah(souradnice)

    def proved_tah(self, start, cil):
        return self.game_manager.proved_tah(start, cil)

    def je_vlastni_figurka(self, souradnice):
        return self.game_manager.je_vlastni_figurka(souradnice)