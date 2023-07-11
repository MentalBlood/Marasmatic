import re
import pathlib
import pydantic
import functools
import dataclasses

from .Text       import Text
from .Pattern    import Pattern
from .Expression import Expression
from .pretags    import PreTags, Constants



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Input:

	source      : frozenset[pathlib.Path]
	expressions : frozenset[Expression]
	pretags     : PreTags   = dataclasses.field(default_factory = dict)
	constants   : Constants = dataclasses.field(default_factory = dict)

	@functools.cached_property
	def expression(self):
		expressions = set(self.expressions)
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

			for match in re.findall(
				self.expression.value,
				Text(
					p.read_text(encoding = 'utf8')
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

			yield None