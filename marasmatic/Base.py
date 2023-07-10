import random
import pydantic
import itertools
import dataclasses

from .Input   import Input
from .Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Base:

	next_  : dict[Pattern, set[Pattern]] = dataclasses.field(default_factory = dict)
	source : Input | None

	def __post_init__(self):
		match self.source:
			case Input():
				for previous, current in itertools.pairwise(self.source.stream):
					self.add(
						previous = previous,
						current  = current
					)
			case _:
				pass

	def add(self, previous: Pattern | None, current: Pattern):

		if previous:
			if previous in self.next_:
				self.next_[previous].add(current)
			else:
				self.add(None, previous)

		if current not in self.next_:
			self.next_[current] = set()

	def next(self, current: Pattern | None) -> Pattern:

		if current in self.next_:
			if len(self.next_[current]):
				return random.choice((*self.next_[current],))

		return random.choice((*self.next_.keys(),))

	@property
	def stream(self, current: Pattern | None = None):
		while True:
			yield (current := self.next(current))