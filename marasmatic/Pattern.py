import pydantic
import pydantic_core

from .Expression import Expression



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Pattern:

	expression : Expression
	value      : str

	@pydantic.field_validator('value', mode = 'after')
	def value_valid(cls, value: str, info: pydantic_core.core_schema.FieldValidationInfo) -> str:
		if not info.data['expression'].match(value):
			raise ValueError
		return value