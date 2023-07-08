import re
import typing
import pydantic
import functools



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Expression:

	value : str

	@functools.cached_property
	def compiled(self):
		return re.compile(self.value)

	@property
	def capturing(self):
		if Expression(r'(?:[^\(\)]+$)|(?:\(\?.+)').match(self.value):
			return Expression(f'({self.value})')
		else:
			return Expression(self.value)

	def __or__(self, another: typing.Self):
		return Expression(f'{self.capturing.value}|{another.capturing.value}')

	def __add__(self, another: typing.Self):
		return Expression(f'{self.value}{another.value}')

	def __mul__(self, n: int):
		result = self
		for _ in range(n - 1):
			result += self
		return result

	def match(self, s: str):
		return re.match(
			pattern = self.compiled,
			string  = s
		) != None