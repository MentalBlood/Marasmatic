import time
import typing
import pydantic
import datetime



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Repeater:

	f        : typing.Callable[[], None]
	interval : datetime.timedelta

	def __call__(self):

		start    = datetime.datetime.now()
		launched = 0

		while True:

			self.f()
			launched += 1

			time.sleep(
				(
					self.interval -
					(
						datetime.datetime.now() - start -
						self.interval * launched
					)
				).seconds
			)
