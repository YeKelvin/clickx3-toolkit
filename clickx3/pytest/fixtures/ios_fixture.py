#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ios_fixture.py
# @Time    : 2021/5/6 17:16
# @Author  : Kelvin.Ye
import pytest


@pytest.fixture(scope='session')
def ios_serial():
    ...
