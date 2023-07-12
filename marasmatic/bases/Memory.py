import random
import pydantic
import dataclasses

from ..Base    import Base
from ..Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Memory(Base):

	next_  : dict[Pattern, set[Pattern]] = dataclasses.field(default_factory = dict)

	def add(self, previous: Pattern | None, current: Pattern):

		if previous:
			if previous in self.next_:
				self.next_[previous].add(current)
			else:
				self.add(None, previous)

		if current not in self.next_:
			self.next_[current] = set()

	def next(self, current: Pattern | None) -> Pattern:

		try:
			if current is not None:
				return random.choice((*self.next_[current],))
		except Exception:
			pass

		return random.choice((*self.next_.keys(),))