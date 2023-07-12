import pytest
import pathlib
import itertools

from .. import marasmatic



@pytest.fixture
def base():
	return marasmatic.bases.Memory(
		source = marasmatic.Input(
			source = frozenset(pathlib.Path('trash/songs').glob('*.txt')),
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