import typing
import pydantic
import dataclasses
import pydantic_core

from .Expression import Expression



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Pattern:

	expression : Expression
	value      : str

	Tags       = dict[str, str]
	tags       : Tags = dataclasses.field(default_factory = dict)

	@pydantic.field_validator('value', mode = 'after')
	def value_valid(cls, value: str, info: pydantic_core.core_schema.FieldValidationInfo) -> str:
		if not info.data['expression'].match(value):
			raise ValueError
		return value

	def tagged(self, tags: Tags):
		return dataclasses.replace(
			self,
			tags = tags
		)

	def __hash__(self):
		return hash(self.value)

	def __eq__(self, another: typing.Self):
		return self.value == another.value