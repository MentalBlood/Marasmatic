import pydantic

from .Pattern import Pattern



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Pair:

	previous : Pattern | None
	current  : Pattern