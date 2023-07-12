import random
import typing
import pathlib
import pydantic

from ..Pair    import Pair
from ..Base    import Base
from ..Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Dir(Base):

	root : pathlib.Path

	def __truediv__(self, key: str):
		return self.root / key

	def __contains__(self, key: str):
		return (self / key).exists()

	def __rshift__(self, key: str):
		return Pattern(
			value = key,
			tags  = {
				k.stem: k.read_text()
				for k in (self / key / 'tags').iterdir()
			}
		)

	def __getitem__(self, key: Pattern):
		return (
			p.stem
			for p in (self / key.value / 'next').iterdir()
		)

	@property
	def keys(self):
		return (
			p.stem
			for p in self.root.iterdir()
		)

	def __ilshift__(self, p: Pair) -> typing.Self:

		if not (tags := self / p.current.value / 'tags').exists():

			tags.mkdir(parents = True)

			for k, v in p.current.tags:
				(tags / k).with_suffix('.txt').write_text(v)

		if p.previous:
			if not (link := self / p.previous.value / "next" / p.current.value).exists():
				link.mkdir(parents = True)

		return self

	def next(self, current: Pattern | None) -> Pattern:

		try:
			if current is not None:
				return self >> random.choice((*self[current],))
		except Exception:
			pass

		return self >> random.choice((*self.keys,))