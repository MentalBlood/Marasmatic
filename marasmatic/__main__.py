import click
import pathlib
import datetime
import itertools

from .bot      import Bot, Repeater

from .         import pretags
from .Input    import Input
from .bases    import Memory, Dir



@click.group
def cli():
	pass


@cli.command(name = 'print')
@click.option('--length', required = True, type = click.IntRange(min = 1), default = 30, show_default = True, help = 'Length of text to generate')
@click.argument("input",  required = True, type = pathlib.Path,            nargs = -1)
def generate(input: tuple[str], length: int):
	print(
		' '.join(
			e.value
			for e in itertools.islice(
				Dir(
					root = pathlib.Path('trash') / 'dir'
				).stream,
				length
			)
		)
	)


@cli.command(name = 'bot')
@click.option('--length',   default = 30, help = 'Length of text to generate',                required = True)
@click.option('--input',                  help = 'Input files paths',                         required = True)
@click.argument("input",                  nargs = -1)
@click.option('--token',                  help = 'Telegram bot token',                        required = True)
@click.option('--interval', default = 30, help = 'Interval between posts, in seconds',        required = True)
@click.option('--chat',                   help = 'Telegram chat id',                          required = True)
@click.option('--site',                   help = 'Site to join file paths to get links with', required = False)
def bot(input: tuple[str], length: int, token: str, chat: str, interval: int, site: str):

	base = Memory(
		source = Input(
			source  = frozenset(map(pathlib.Path, input)),
			pretags = {
				'file' : pretags.file,
				'link' : pretags.link
			},
			constants = {
				'site' : site
			}
		)
	)

	Repeater(
		f = lambda: Bot(
			token = token,
			chat  = chat
		).send(
			' '.join(

				     f"<a href='{e.tags['link']}'>{e.value}</a>"
				if   e.tags['link']
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