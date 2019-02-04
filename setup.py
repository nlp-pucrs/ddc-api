from setuptools import setup, Command
import subprocess

## based on https://github.com/jpvanhal/flask-split

class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)


setup(
    name='DDC API',
    version='0.1b',
    url='https://github.com/nlp-pucrs/ddc-api',
    license='AGPL-3.0',
    author='Henrique Dias',
    author_email='henrique.santos.003@acad.pucrs.br',
    description='Flask API for DDC Prescription Score',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
    ],
    cmdclass={'test': PyTest},
)
