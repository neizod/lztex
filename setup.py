from distutils.core import setup

setup( name = 'lztex',
       version = 'nighty',
       description = 'LzTeX: markdown style LaTeX.',
       author = 'Nattawut Phetmak',
       license = 'WTFPL v2.0',
       packages = ['lztex'],
       scripts = ['bin/lztex'],
       install_requires = ['ply'],
     )
