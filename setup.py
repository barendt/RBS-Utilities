from distutils.core import setup, Extension

c_strings = Extension('cStrings',
                      sources = ['rbs/cStrings.c'])

setup(name='rbs',
      version='1.0',
      py_modules = [
        'rbs.Constants',
        'rbs.Exceptions',
        'rbs.Files',
        'rbs.Phage',
        'rbs.Sequences',
        'rbs.Strings',
        'rbs.Transterm',
        'rbs.Utilities',],
      ext_modules = [c_strings],
      ext_package = 'rbs',
      #packages = ['rbs'],
      )
