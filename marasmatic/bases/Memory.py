import random
import typing
import pydantic

from ..Pair    import Pair
from ..Base    import Base
from ..Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Memory(Base, dict[Pattern, set[Pattern]]):

	def __ilshift__(self, p: Pair) -> typing.Self:

		if p.previous:
			if p.previous in self:
				self[p.previous].add(p.current)
			else:
				self <<= Pair(None, p.previous)

		if p.current not in self:
			self[p.current] = set()

		return self

	def next(self, current: Pattern | None) -> Pattern:

		try:
			if current is not None:
				return random.choice((*self[current],))
		except Exception:
			pass

		return random.choice((*self.keys(),))