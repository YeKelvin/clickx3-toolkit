#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : exceptions.py
# @Time    : 2019/8/30 10:51
# @Author  : Kelvin.Ye
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class AppException(Exception):
    pass


class PageException(Exception):
    pass


class ElementException(Exception):
    pass


class OCRException(Exception):
    pass


class OCRRetriesExceededException(Exception):
    pass
