import pydantic



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Punctuation:

	middle : frozenset[str]
	end    : frozenset[str]