#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : variable_fixture.py
# @Time    : 2021/5/1 13:42
# @Author  : Kelvin.Ye
import pytest

from clickx3.utils.log_util import get_logger
from clickx3.utils.yaml_util import load_env_config


log = get_logger(__name__)


@pytest.fixture(scope='session', autouse=True)
def props(env):
    """全局变量"""
    env_config = load_env_config(env)
    env_config['env'] = env
    return env_config


@pytest.fixture(scope='class', autouse=True)
def vars():
    """局部变量"""
    return {}
