#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : yaml_util.py
# @Time    : 2021/4/10 21:39
# @Author  : Kelvin.Ye
import os
from functools import lru_cache

import yaml

from clickx3.utils import project


def load(stream):
    """反序列化"""
    if stream.endswith('.yaml'):
        with open(stream, mode='r', encoding='utf8') as file:
            stream = file.read()
            return yaml.safe_load(stream)

    return yaml.safe_load(stream)


def dump(data):
    """序列化"""
    return yaml.safe_dump(data, encoding='utf-8')


@lru_cache
def load_env_config(name):
    if not name:
        raise FileNotFoundError('yaml配置文件名称不允许为空')

    if not name.endswith('.yaml'):
        name = name + '.yaml'

    file_path = os.path.join(project.environment_path(), name)
    return load(file_path)
