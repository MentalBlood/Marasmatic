import pydantic
import requests



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Bot:

	token : str
	chat  : str

	def send(self, message: str):
		requests.post(
			f'https://api.telegram.org/bot{self.token}/sendMessage',
			data  = {
				'chat_id'              : self.chat,
				'text'                 : message,
				'disable_notification' : True
			}
		)
