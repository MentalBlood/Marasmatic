import pathlib
import pydantic

from .Token       import Token
from .Punctuation import Punctuation



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Input:

	source      : frozenset[pathlib.Path]
	encoding    : frozenset[str]
	letters     : frozenset[str]          = frozenset('йцукенгшщзхфывапролджэячсмитьбюъё')
	punctuation : Punctuation             = Punctuation(middle = frozenset('-—'), end = frozenset('.!?'))

	@property
	def stream(self):

		for p in self.source:

			word = ''

			for e in self.encoding:

				try:

					with p.open('r', encoding = e) as f:

						while _c := f.read(1):

							c = _c.lower()

							if c in self.letters:
								word += c
								continue

							if word:
								yield Token(word, p)
								word = ''

							if c in self.punctuation.middle:
								yield Token(c, p)
							elif c in self.punctuation.end:
								yield Token(c, p)
								yield None

					break

				except Exception:
					continue

			yield None