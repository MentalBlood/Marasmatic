import typing
import pydantic

from ..Token import Token



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Message:

	source : str | typing.Sequence[Token]
	site   : str | None

	@property
	def content(self):
		match self.source:
			case str():
				return self.source
			case _:
				return ' '.join(

						f"<a href='{e.link(self.site)}'>{e.value}</a>"
					if   self.site
					else e.value

					for e in self.source

				)