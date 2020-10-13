#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Page:
    url = None

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value
        if self.driver:
            for attr in self.__dict__.values():
                if isinstance(attr, self.__class__):
                    attr.device = value

    def __init__(self, driver=None):
        if driver:
            self._driver = driver

    def get(self):
        if self.url:
            self.driver.get(self.hostname + self.url)
