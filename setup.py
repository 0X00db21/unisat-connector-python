#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='unisat-connector-python',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    license='BSD 3-Clause License'
)
