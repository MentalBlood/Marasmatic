import random
import typing
import pathlib
import pydantic

from ..Base    import Base
from ..Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Dir(Base):

	root : pathlib.Path

	def path(self, key: Pattern | str):
		match key:
			case Pattern():
				return self.root / key.value
			case str():
				return self.root / key

	def __contains__(self, key: Pattern):
		return self.path(key).exists()

	@typing.overload
	def __getitem__(self, key: Pattern) -> typing.Generator[str, None, None]:
		pass

	@typing.overload
	def __getitem__(self, key: str) -> Pattern:
		pass

	def __getitem__(self, key: Pattern | str):
		match key:
			case Pattern():
				return (
					p.stem
					for p in self.path(key).iterdir()
				)
			case str():
				return Pattern(
					value = key,
					tags = {
						k.stem: k.read_text()
						for k in (self.path(key) / 'tags').iterdir()
					}
				)

	def keys(self):
		return (
			p.stem
			for p in self.root.iterdir()
		)

	def append(self, e: Pattern):

		if (tags := (self.path(e) / 'tags')).exists():
			return

		tags.mkdir(parents = True)

		for k, v in e.tags:
			(tags / k).with_suffix('.txt').write_text(v)

	def add(self, previous: Pattern | None, current: Pattern):

		if current not in self:
			self.append(current)

		if previous:
			if previous in self:
				(self.path(previous) / current.value).link_to(self.path(current))
			else:
				self.add(None, previous)

	def next(self, current: Pattern | None) -> Pattern:

		try:
			if current is not None:
				return self[random.choice((*self[current],))]
		except Exception:
			pass

		return self[random.choice((*self.keys(),))]