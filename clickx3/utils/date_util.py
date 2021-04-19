#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : date_util.py
# @Time    : 2021/4/19 18:47
# @Author  : Kelvin.Ye
import datetime


def today(strformat=None):
    if strformat:
        return datetime.date.today().strftime(strformat)
    return datetime.date.today()
