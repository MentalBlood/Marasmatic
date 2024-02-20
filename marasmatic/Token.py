import typing
import pathlib
import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=False)
class Token:
    value: str
    path: pathlib.Path

    def link(self, site: str):
        return f"{site}{self.path.stem.replace('___', '/')}.html"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, another: typing.Self):
        return self.value == another.value
