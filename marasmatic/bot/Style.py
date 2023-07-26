import typing

from ..Token import Token

from .Word import Word



Style = typing.Callable[[Token, str], Word]