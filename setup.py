from distutils.core import setup

setup(name='subtitlestools',
      version='0.1',
      description='Libary for manipulate movie subtitels',
      url='https://bitbucket.org/angrysoft/subtitles-tools',
      author='Sebastian Zwierzchwoski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      package_dir={'subtitlestools' : 'src'},
      packages=['subtitlestools'],
      sctipts=['apps/napi-cli.py'])
