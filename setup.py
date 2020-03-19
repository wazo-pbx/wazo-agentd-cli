#!/usr/bin/env python3
# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo-agentd-cli',
    version='1.0',

    description='a CLI program to interact with a wazo-agentd server',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),
    scripts=['bin/wazo-agentd-cli', 'bin/xivo-agentd-cli'],
)
