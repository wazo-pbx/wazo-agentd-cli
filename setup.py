#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='xivo-agentd-cli',
    version='1.0',

    description='a CLI program to interact with a xivo-agentd server',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),
    scripts=['bin/xivo-agentd-cli'],
)
