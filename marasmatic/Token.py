import typing
import pathlib
import pydantic



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Token:

	value : str
	path  : pathlib.Path

	def __hash__(self):
		return hash(self.value)

	def __eq__(self, another: typing.Self):
		return self.value == another.value