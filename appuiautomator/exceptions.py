#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : exceptions.py
# @Time    : 2019/8/30 10:51
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class AppError(Exception):
    pass


class PageError(Exception):
    pass


class PageElementError(Exception):
    pass


class PageElementsError(Exception):
    pass


class XPathElementError(Exception):
    pass


class XPathElementsError(Exception):
    pass
