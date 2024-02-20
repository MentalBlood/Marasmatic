import abc
import dataclasses
import itertools
import typing

from .Input import Input
from .Pair import Pair
from .Token import Token


@dataclasses.dataclass(frozen=True, kw_only=False)
class Base(metaclass=abc.ABCMeta):
    source: Input | None = None

    def __post_init__(self):
        if self.source:
            for previous, current in itertools.pairwise(self.source.stream):
                if current is not None:
                    self <<= Pair(previous, current)

    @abc.abstractmethod
    def __ilshift__(self, p: Pair) -> typing.Self:
        ...

    @abc.abstractmethod
    def next(self, current: Token | None) -> Token:
        ...

    @property
    def stream(self, current: Token | None = None):
        while True:
            yield (current := self.next(current))
