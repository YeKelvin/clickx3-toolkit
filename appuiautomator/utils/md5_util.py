#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : md5_util
# @Time    : 2020/9/8 20:48
# @Author  : Kelvin.Ye
import hashlib


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
