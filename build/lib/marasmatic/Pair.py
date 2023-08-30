import pydantic

from .Token import Token



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Pair:

	previous : Token | None
	current  : Token