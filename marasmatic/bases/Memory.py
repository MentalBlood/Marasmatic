import random
import typing
import pydantic
import dataclasses

from ..Pair    import Pair
from ..Base    import Base
from ..Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Memory(Base):

	next_  : dict[Pattern, set[Pattern]] = dataclasses.field(default_factory = dict)

	def __ilshift__(self, p: Pair) -> typing.Self:

		if p.previous:
			if p.previous in self.next_:
				self.next_[p.previous].add(p.current)
			else:
				self <<= Pair(None, p.previous)

		if p.current not in self.next_:
			self.next_[p.current] = set()

		return self

	def next(self, current: Pattern | None) -> Pattern:

		try:
			if current is not None:
				return random.choice((*self.next_[current],))
		except Exception:
			pass

		return random.choice((*self.next_.keys(),))