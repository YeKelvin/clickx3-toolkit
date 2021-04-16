#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : dict_util
# @Time    : 2020/9/9 14:54
# @Author  : Kelvin.Ye


def sort_dict(obj: dict):
    if not obj:
        return None
    return dict(sorted(obj.items(), key=lambda d: d[0]))
