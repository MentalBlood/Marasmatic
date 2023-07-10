import pydantic

from .Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Marasm:

	content : tuple[Pattern]

	def __str__(self):
		return ' '.join(
			p.value
			for p in self.content
		)