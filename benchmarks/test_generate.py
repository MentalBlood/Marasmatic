import pytest
import pathlib
import itertools

from .. import marasmatic



@pytest.fixture
def base():
	return marasmatic.Base(
		source = marasmatic.Input(
			source      = set(pathlib.Path('trash/songs').glob('*.txt')),
			expressions = {
				marasmatic.expressions.Word,
				marasmatic.expressions.PunctuationMark
			}
		)
	)


@pytest.mark.benchmark(group = 'generate')
def test_generate(benchmark, base: marasmatic.Input):

	def generate():
		for _ in itertools.islice(
			base.stream,
			1000000
		):
			continue

	benchmark(generate)