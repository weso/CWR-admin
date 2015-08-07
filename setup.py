# -*- coding: utf-8 -*-
import ast
import re
from codecs import open
from os import path

from setuptools import setup, find_packages

"""
PyPI configuration module.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__version__ = '0.0.0'

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_tests_require = ['pytest', 'nose', 'Flask-Testing']

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open('cwr_admin/__init__.py', 'rb', encoding='utf-8') as f:
    version = f.read()
    version = _version_re.search(version).group(1)
    version = str(ast.literal_eval(version.rstrip()))

setup(
    name='CWR-Admin-WS',
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },
    version=version,
    description='Administration web service for CWR files',
    author='WESO',
    author_email='weso@weso.es',
    license='MIT',
    url='https://github.com/weso/CWR-Validator',
    download_url='https://github.com/weso/CWR-Validator',
    keywords=['CWR', 'commonworks', 'api', 'CISAC', 'validator'],
    platforms='any',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: Implementation :: PyPy'],
    long_description=long_description,
    install_requires=[
        'Flask',
        'Flask-RESTful',
        'CWR-API',
    ],
    tests_require=_tests_require,
    extras_require={'test': _tests_require},
)
