import dataclasses

from .Token import Token



@dataclasses.dataclass(frozen = True, kw_only = False)
class Pair:

	previous : Token | None
	current  : Token