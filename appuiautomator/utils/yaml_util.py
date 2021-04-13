#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : time_util.py
# @Time    : 2021/4/10 21:39
# @Author  : Kelvin.Ye
import os

import yaml
from appuiautomator.utils.config import resources_path


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


# TODO: 加结果缓存
def load_testdata(name):
    if not name.endswith('.yaml'):
        name = name + '.yaml'
    file_path = os.path.join(resources_path(), 'testdata', name)
    return load(file_path)
