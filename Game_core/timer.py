from typing import Optional
import time

class Timer:
    def __init__(self, vychozi_sekundy: int = 300):
        self.vychozi_sekundy = vychozi_sekundy
        self.cas_hrac = [float(vychozi_sekundy), float(vychozi_sekundy)]
        self.bezi = False
        self._start: Optional[float] = None

    def prepni(self, hrac: int) -> None:
        if self.bezi and self._start is not None:
            uplynulo = time.monotonic() - self._start
            self.cas_hrac[hrac] = max(0.0, self.cas_hrac[hrac] - uplynulo)
        self._start = time.monotonic()
        self.bezi = True

    def zbyva(self, hrac: int) -> float:
        if self.bezi and self._start is not None:
            return max(0.0, self.cas_hrac[hrac] - (time.monotonic() - self._start))
        return self.cas_hrac[hrac]

    def vyprsel(self, hrac: int) -> bool:
        return self.zbyva(hrac) <= 0.0

    def nuluj(self) -> None:
        self.cas_hrac = [float(self.vychozi_sekundy), float(self.vychozi_sekundy)]
        self.bezi = False
        self._start = None