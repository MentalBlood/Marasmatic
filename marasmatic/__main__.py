import click
import pathlib
import datetime
import itertools

from .bot   import Bot, Repeater

from .Input import Input
from .bases import Memory



@click.group
def cli():
	pass


@cli.command(name = 'print')
@click.option('--length', required = True, type = click.IntRange(min = 1), default = 30, show_default = True, help = 'Length of text to generate')
@click.argument("input",  required = True, type = pathlib.Path,            nargs = -1)
def generate(input: tuple[pathlib.Path], length: int):
	print(
		' '.join(
			e.value
			for e in itertools.islice(
				Memory(
					source = Input(
						source = frozenset(input)
					)
				).stream,
				length
			)
		)
	)


@cli.command(name = 'bot')
@click.option('--length',   required = True,  type = click.IntRange(min = 1), default = 30, show_default = True, help = 'Length of text to generate')
@click.argument("input",    required = True,  type = pathlib.Path,            nargs = -1)
@click.option('--token',    required = True,  type = str,                                                        help = 'Telegram bot token')
@click.option('--interval', required = True,  type = click.IntRange(min = 1), default = 30, show_default = True, help = 'Interval between posts, in seconds')
@click.option('--chat',     required = True,  type = str,                                                        help = 'Telegram chat id')
@click.option('--site',     required = False, type = str,                                                        help = 'Site to join file paths to get links with')
def bot(input: tuple[pathlib.Path], length: int, token: str, chat: str, interval: int, site: str):

	base = Memory(
		source = Input(
			source  = frozenset(input)
		)
	)

	Repeater(
		f = lambda: Bot(
			token = token,
			chat  = chat
		).send(
			' '.join(

				     f"<a href='{site}{e.path.stem.replace('___', '/')}.html'>{e.value}</a>"
				if   site
				else e.value

				for e in itertools.islice(
					base.stream,
					length
				)

			)
		),
		interval = datetime.timedelta(seconds = interval)
	)()


cli()