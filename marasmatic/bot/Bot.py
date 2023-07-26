import pydantic
import requests

from .Message import Message



@pydantic.dataclasses.dataclass(frozen = True, kw_only = True)
class Bot:

	token : str
	chat  : str

	def send(self, message: Message):
		requests.post(
			f'https://api.telegram.org/bot{self.token}/sendMessage',
			data  = {
				'chat_id'              : self.chat,
				'text'                 : message.content,
				'parse_mode'           : 'html',
				'disable_web_page_preview': 'true'
			}
		)