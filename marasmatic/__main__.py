import click
import pathlib
import datetime
import itertools

from .bot      import Bot, Repeater

from .Base     import Base
from .Input    import Input
from .patterns import PunctuationMark, Word



@click.group
def cli():
	pass


@cli.command(name = 'print')
@click.option('--length', default = 30, help = 'Length of text to generate', required = True)
@click.option('--input',                help = 'Input file',                 required = True)
def generate(input: pathlib.Path, length: int):
	print(
		' '.join(
			e.value
			for e in itertools.islice(
				Base(
					source = Input(
						source      = input,
						expressions = {
							Word,
							PunctuationMark
						}
					)
				).stream,
				length
			)
		)
	)


@cli.command(name = 'bot')
@click.option('--length',   default = 30, help = 'Length of text to generate',         required = True)
@click.option('--input',                  help = 'Input file',                         required = True)
@click.option('--token',                  help = 'Telegram bot token',                 required = True)
@click.option('--interval', default = 30, help = 'Interval between posts, in seconds', required = True)
@click.option('--chat',                   help = 'Telegram chat id',                   required = True)
def bot(input: pathlib.Path, length: int, token: str, chat: str, interval: int):

	base = Base(
		source = Input(
			source      = input,
			expressions = {
				Word,
				PunctuationMark
			}
		)
	)

	Repeater(
		f = lambda: Bot(
			token = token,
			chat  = chat
		).send(
			' '.join(
				e.value
				for e in itertools.islice(
					base.stream,
					length
				)
			)
		),
		interval = datetime.timedelta(seconds = interval)
	)()


cli()