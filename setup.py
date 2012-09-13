#!/usr/bin/env python

import os, sys
import wiretransfers

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

packages = [
    'wiretransfers',
]

requires = [
    'pycrypto >= 2.5'
]

setup(
    name='wiretransfers',
    version=wiretransfers.__version__,
    description='Simple API for IPizza Solo/TUPAS payment protocols.',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Priit Laes',
    author_email='plaes@plaes.org',
    url='http://plaes.org/projects/wiretransfers',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'wiretransfers': 'wiretransfers'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)

del os.environ['PYTHONDONTWRITEBYTECODE']
