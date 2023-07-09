import pydantic



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Tag:

	value : str