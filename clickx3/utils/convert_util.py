#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : convert_util.py
# @Time    : 2021/5/10 10:07
# @Author  : Kelvin.Ye
from distutils.util import strtobool


def str_to_bool(val):
    return bool(strtobool(val))
