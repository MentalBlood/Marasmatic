import re
import typing
import pydantic



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Expression:

	value : str

	@classmethod
	def joined(cls, expressions: typing.Iterable['Expression']):
		return Expression(
			'|'.join(
				a.value
				for a in expressions
			)
		)

	def match(self, s: str):
		return re.match(
			pattern = self.value,
			string  = s
		) != None

	def filter(self, s: str):
		return (
			match
			for match in re.findall(r'.*?(' + self.value + r').*?(?: |\n|$)', s)
			if match
		)