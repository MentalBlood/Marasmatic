import pathlib
import pydantic
import dataclasses

from .Pattern    import Pattern
from .pretags    import PreTags, Constants



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Input:

	source      : frozenset[pathlib.Path]
	letters     : frozenset[str]          = frozenset('йцукенгшщзхфывапролджэячсмитьбюъё')
	punctuation : frozenset[str]          = frozenset('.-—!?')
	pretags     : PreTags                 = dataclasses.field(default_factory = dict)
	constants   : Constants               = dataclasses.field(default_factory = dict)

	@property
	def stream(self):

		for p in self.source:

			tags = {
				key: value(p, self.constants, self.pretags)
				for key, value in self.pretags.items()
			}

			word = ''

			for _c in p.read_text(encoding = 'utf8'):

				c = _c.lower()

				if c in self.letters:
					word += c
					continue

				if word:
					yield Pattern(
						value = word,
						tags  = tags
					)
					word = ''

				if c in self.punctuation:
					yield Pattern(
						value = c,
						tags  = tags
					)

			yield None