import datetime
import itertools
import pathlib
import pickle

import click

from . import bases
from .bot import Bot, Message, Repeater
from .Input import Input


@click.group
def cli():
    pass


@cli.command(name="print")
@click.option(
    "--length",
    required=True,
    type=click.IntRange(min=1),
    default=30,
    show_default=True,
    help="Length of text to generate",
)
@click.argument("input", required=True, type=pathlib.Path, nargs=-1)
@click.option("--encoding", required=True, type=str, default=("utf8",), help="Input files encoding", multiple=True)
def generate(input: tuple[pathlib.Path], encoding: tuple[str], length: int):
    print(
        Message(
            site=None,
            source=[
                *itertools.islice(
                    bases.Memory(Input(source=frozenset(input), encoding=frozenset[str](encoding))).stream, length
                )
            ],
        ).content
    )


@cli.command(name="serialize")
@click.argument("input", required=False, type=pathlib.Path, nargs=-1)
@click.option("--encoding", required=True, type=str, default=("utf8",), help="Input files encoding", multiple=True)
@click.option("--output", required=False, type=pathlib.Path, default=None, help="Output file path")
def serialize(input: tuple[pathlib.Path], encoding: tuple[str], output: pathlib.Path):
    output.write_bytes(pickle.dumps(bases.Memory(Input(source=frozenset(input), encoding=frozenset[str](encoding)))))


@cli.command(name="bot")
@click.option(
    "--length",
    required=True,
    type=click.IntRange(min=1),
    default=30,
    show_default=True,
    help="Length of text to generate",
)
@click.argument("input", required=False, type=pathlib.Path, nargs=-1)
@click.option("--token", required=True, type=str, help="Telegram bot token")
@click.option(
    "--interval",
    required=True,
    type=click.IntRange(min=1),
    default=30,
    show_default=True,
    help="Interval between posts, in seconds",
)
@click.option("--chat", required=True, type=str, help="Telegram chat id")
@click.option("--site", required=False, type=str, help="Site to join file paths to get links with")
@click.option("--encoding", required=True, type=str, default=("utf8",), help="Input files encoding", multiple=True)
@click.option("--pickled", required=False, type=pathlib.Path, default=None, help="Path to serialized base")
@click.option("--one/--loop", required=True, default=("--loop",), help="Post one message or run endless loop")
def bot(
    input: tuple[pathlib.Path],
    encoding: tuple[str],
    length: int,
    token: str,
    chat: str,
    interval: int,
    site: str,
    one: bool,
    pickled: pathlib.Path | None,
):
    if pickled is None:
        base = bases.Memory(Input(source=frozenset(input), encoding=frozenset[str](encoding)))
    else:
        base: bases.Memory = pickle.loads(pickled.read_bytes())

    f = lambda: Bot(token=token, chat=chat).send(Message(site=site, source=[*itertools.islice(base.stream, length)]))

    if one:
        f()
    else:
        Repeater(f=f, interval=datetime.timedelta(seconds=interval))()


cli()
