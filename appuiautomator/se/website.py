#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class WebSite:
    hostname = None

    def __init__(self, driver):
        self.driver = driver
