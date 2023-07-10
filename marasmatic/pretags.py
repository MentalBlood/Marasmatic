import typing
import pathlib
import pydantic



Constant  = str
Constants = dict[str, Constant]


@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class PreTag:

	f : typing.Callable[[pathlib.Path, Constants, 'PreTags'], str]

	def __call__(self, p: pathlib.Path, c: Constants, t: 'PreTags'):
		try:
			return self.f(p, c, t)
		except Exception:
			return None


PreTags   = dict[str, PreTag]

file   = PreTag(lambda p, c, t: p.name)
source = PreTag(lambda p, c, t: p.read_text())
link   = PreTag(lambda p, c, t: f"{c['site']}{pathlib.Path(t['file'].f(p, c, t)).stem.replace('___', '/')}.html")