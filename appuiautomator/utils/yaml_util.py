#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : time_util.py
# @Time    : 2021/4/10 21:39
# @Author  : Kelvin.Ye
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load(stream):
    """反序列化"""
    return yaml.load(stream, Loader=Loader)


def dump(data):
    """序列化"""
    return yaml.dump(data, Dumper=Dumper, encoding='utf-8')
