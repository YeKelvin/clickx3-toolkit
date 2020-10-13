#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Page:
    url = None

    def __init__(self, driver):
        self.driver = driver

    def get(self):
        if self.url:
            self.driver.get(self.hostname + self.uri)
