#!/usr/bin/env python

from setuptools import setup

setup(
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
