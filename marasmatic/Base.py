import abc
import pydantic
import itertools

from .Input   import Input
from .Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Base(metaclass = abc.ABCMeta):

	source : Input | None

	def __post_init__(self):
		match self.source:
			case Input():
				for previous, current in itertools.pairwise(self.source.stream):
					if current is not None:
						self.add(
							previous = previous,
							current  = current
						)
			case _:
				pass

	@abc.abstractmethod
	def add(self, previous: Pattern | None, current: Pattern) -> None:
		...

	@abc.abstractmethod
	def next(self, current: Pattern | None) -> Pattern:
		...

	@property
	def stream(self, current: Pattern | None = None):
		while True:
			yield (current := self.next(current))