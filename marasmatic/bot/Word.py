import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=False)
class Word:
    value: str

    def link(self, address: str):
        return Word(f"<a href='{address}'>{self.value}</a>")

    @property
    def bold(self):
        return Word(f"<b>{self.value}</b>")

    @property
    def italic(self):
        return Word(f"<i>{self.value}</i>")
