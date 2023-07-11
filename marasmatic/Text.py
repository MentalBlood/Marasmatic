import re
import pydantic

from .Expression import Expression



@pydantic.dataclasses.dataclass(frozen = True, kw_only = False)
class Text:

	content : str

	def cleaned(self, leave: Expression):
		return ' '.join(
			m
			for m in re.findall(
				leave.value,
				self.content.lower().replace('\n', ' ').replace(',', '')
			)
		)