from distutils.core import setup
#files=['apps/napi-cli.py', 'README.pl']

setup(name='subtitlestools',
      version='0.2',
      description='Libary for manipulate movie subtitels',
      url='https://bitbucket.org/angrysoft/subtitles-tools',
      author='Sebastian Zwierzchwoski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      package_dir={'subtitlestools' : 'src'},
      packages=['subtitlestools'],
      scripts=['apps/napi-cli.py'])
