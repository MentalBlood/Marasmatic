import re
import pathlib
import pydantic

from .Text       import Text
from .Pattern    import Pattern
from .Expression import Expression



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Input:

	source      : set[pathlib.Path]
	expressions : set[Expression]

	@property
	def expression(self):
		expressions = self.expressions.copy()
		result      = expressions.pop()
		for e in expressions:
			result |= e
		return result

	def classify(self, s: str):

		for e in self.expressions:
			if e.match(s):
				return Pattern(
					value      = s,
					expression = e
				)

		raise ValueError(f'Can not classify pattern with value `{s}`')

	@property
	def stream(self):
		for p in self.source:
			text = p.read_text(encoding = 'utf8')
			for match in re.findall(
				self.expression.value,
				Text(
					text
				).cleaned(
					leave = self.expression
				)
			):
				for m in match:
					if len(m):
						yield self.classify(m).tagged({
							'file': p.name,
							'source': text
						})
						break