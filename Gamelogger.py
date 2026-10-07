class GameLogger:

    def __init__(self):
        self.log = []

    def uloz(self, zprava):
        cas = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{cas}] {zprava}")

    def vrat_log(self):
        return list(self.log)
