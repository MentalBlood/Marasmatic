import re
import pydantic

from .Expression import Expression



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Text:

	content : str

	def cleaned(self, leave: Expression):
		return ' '.join(
			s
			for m in re.findall(
				leave.value,
				self.content.lower().replace('\n', ' ').replace(',', '')
			)
			for s in m
			if len(s)
		)