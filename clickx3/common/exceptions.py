#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : exceptions.py
# @Time    : 2019/8/30 10:51
# @Author  : Kelvin.Ye


class AppException(Exception):
    pass


class PageException(Exception):
    pass


class ElementException(Exception):
    pass


class TimeoutException(Exception):
    pass


class OCRException(Exception):
    pass


class OCRRetriesExceededException(Exception):
    pass


class ProjectBaseDirectoryNotFoundException(Exception):
    ...
