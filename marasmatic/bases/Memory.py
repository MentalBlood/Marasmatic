import random
import typing
import dataclasses

from ..Pair import Pair
from ..Base import Base
from ..Token import Token


@dataclasses.dataclass(frozen=True, kw_only=False)
class Memory(Base, dict[Token, set[Token]]):
    def __ilshift__(self, p: Pair) -> typing.Self:
        if p.previous:
            if p.previous in self:
                self[p.previous].add(p.current)
            else:
                self <<= Pair(None, p.previous)

        if p.current not in self:
            self[p.current] = set()

        return self

    def random(self, sequence: typing.Sequence[Token], current: Token | None):
        if current is None:
            return random.choice(sequence)
        else:
            other = tuple(e for e in sequence if e.path != current.path)
            if not other:
                return random.choice(sequence)
            else:
                while (result := random.choice(sequence)).path == current.path:
                    continue
                return result

    def next(self, current: Token | None) -> Token:
        try:
            if current is not None:
                return self.random((*self[current],), current)
        except Exception:
            pass

        return self.random((*self.keys(),), current)
