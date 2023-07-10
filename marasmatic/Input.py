import re
import pathlib
import pydantic
import dataclasses

from .Text       import Text
from .Pattern    import Pattern
from .Expression import Expression
from .pretags    import PreTags, Constants



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Input:

	source      : set[pathlib.Path]
	expressions : set[Expression]
	pretags     : PreTags   = dataclasses.field(default_factory = dict)
	constants   : Constants = dataclasses.field(default_factory = dict)

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
							key: value(p, self.constants, self.pretags)
							for key, value in self.pretags.items()
						})
						break