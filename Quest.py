@dataclass
class Quest:
    nazev: str
    popis: str
    splneno: bool = False

    def validate(self) -> bool:
        return self.splneno