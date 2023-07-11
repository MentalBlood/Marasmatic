import typing
import pydantic



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Pattern:

	value : str
	tags  : dict[str, str | None]

	def __hash__(self):
		return hash(self.value)

	def __eq__(self, another: typing.Self):
		return self.value == another.value