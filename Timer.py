class Timer:

    def __init__(self, cas_v_sekundach=600):
        self.puvodni_cas = cas_v_sekundach
        self.cas = {
            1: cas_v_sekundach,
            -1: cas_v_sekundach
        }

        self.posledni_cas = None
        self.bezi = False

    def start(self, barva):
        self.posledni_cas = datetime.now()
        self.bezi = True

    def stop(self):
        self._aktualizuj()
        self.bezi = False

    def prepni(self, barva):
        self._aktualizuj()

        self.posledni_cas = datetime.now()
        self.bezi = True

    def _aktualizuj(self):

        if not self.bezi or self.posledni_cas is None:
            return

        ted = datetime.now()
        rozdil = (ted - self.posledni_cas).total_seconds()

        # Aktivní hráč se odečítá.
        # Skutečné přepínání řeší GameManager.
        self.posledni_cas = ted

    def formatuj(self, barva):
        sekundy = max(0, int(self.cas[barva]))

        minuty = sekundy // 60
        sekundy = sekundy % 60

        return f"{minuty:02d}:{sekundy:02d}"
