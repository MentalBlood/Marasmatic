import pathlib
import setuptools



if __name__ == '__main__':

	packages = setuptools.find_packages(exclude = ['tests*'])

	setuptools.setup(
		name                          = 'marasmatic',
		version                       = '1.3.1',
		description                   = 'Connected drivel generator',
		long_description              = (pathlib.Path(__file__).parent / 'README.md').read_text(),
		long_description_content_type = 'text/markdown',
		author                        = 'mentalblood',
		packages                      = packages,
		install_requires              = [
			'pydantic',
			'click'
		]
	)