from setuptools import setup

requirements = open('requirements.txt').readlines()

setup(name='Spoonerist',
      version='0.1',
      description='Spoonerism Tool',
      author='Scott Wilson',
      author_email='scott.wilson@gmail.com',
      test_suite='tests',
      setup_requires=['pytest-runner', *requirements],
      tests_require=['pytest'],
      url='https://github.com/scottynomad/spoonerist/',
      packages=['spoonerist'],
      )
