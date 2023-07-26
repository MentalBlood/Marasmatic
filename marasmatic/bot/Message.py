import typing
import pydantic

from ..Token import Token

from .Word  import Word
from .Style import Style



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Message:

	source : str | typing.Sequence[Token]
	site   : str | None

	styles : typing.Sequence[Style] = (
		lambda token, site: Word(token.value).link(site),
		lambda token, site: Word(token.value).link(site).bold
	)

	@property
	def content(self):

		match self.source:

			case str():
				return self.source

			case _:

				if self.site is None:
					return ' '.join(
						token.value
						for token in self.source
					)

				else:

					result   : list[str]    = []
					style    : int          = 0
					previous : Token | None = None

					for token in self.source:

						if previous:
							if previous.path != token.path:
								style = (style + 1) % len(self.styles)

						result.append(self.styles[style](token, self.site).value)
						previous = token

					return ' '.join(result)