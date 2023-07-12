import pathlib
import pydantic
import dataclasses

from .Pattern     import Pattern
from .Punctuation import Punctuation
from .pretags     import PreTags, Constants



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Input:

	source      : frozenset[pathlib.Path]
	letters     : frozenset[str]          = frozenset('йцукенгшщзхфывапролджэячсмитьбюъё')
	punctuation : Punctuation             = Punctuation(middle = frozenset('-—'), end = frozenset('.!?'))
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

			with p.open('r', encoding = 'utf8') as f:

				read = 0

				while True:

					if not (read % (1024 * 8)):
						print(read // 1024 * 2)

					if not (_c := f.read(1)):
						break
					read += 1

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

					if c in self.punctuation.middle:
						yield Pattern(
							value = c,
							tags  = tags
						)
					elif c in self.punctuation.end:
						yield None

			yield None