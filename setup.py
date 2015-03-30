#!/usr/bin/env python

__version__ = '1.0.0dev'

from setuptools import setup

setup(
    name='upbrew',
    version=__version__,
    app=['upbrew.py'],
    data_files=[],
    options={
        'py2app': {
            'argv_emulation': True,
            'plist': {
                'LSUIElement': True,
            },
            'packages': ['rumps'],
        },
    },
    setup_requires=['py2app'],
)
