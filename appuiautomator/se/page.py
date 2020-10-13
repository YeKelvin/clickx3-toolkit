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
        if self._driver:
            for attr in self.__dict__.values():
                if isinstance(attr, self.__class__):
                    attr.device = value

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        self._hostname = value
        if self._hostname:
            for attr in self.__dict__.values():
                if isinstance(attr, self.__class__):
                    attr.hostname = value

    def __init__(self, driver=None, hostname=None):
        if driver:
            self._driver = driver
        if hostname:
            self._hostname = hostname

    def get(self):
        if self.hostname and self.url:
            self.driver.get(self.hostname + self.url)
