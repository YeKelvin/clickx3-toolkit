#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : exceptions.py.py
# @Time    : 2019/8/30 10:51
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class PageError(Exception):
    pass


class PageElementError(Exception):
    pass
