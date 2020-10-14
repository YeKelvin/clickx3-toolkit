#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from appuiautomator.se.webdriver import Browser
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Page:
    url = None

    @property
    def browser(self) -> Browser:
        return self._browser

    @browser.setter
    def browser(self, value):
        self._browser = value
        if self._browser:
            for attr in self.__dict__.values():
                if isinstance(attr, self.__class__):
                    attr.browser = value

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

    def __init__(self, browser=None, hostname=None):
        if browser:
            self._browser = browser
        if hostname:
            self._hostname = hostname

    def get(self):
        if self.hostname and self.url:
            self.browser.driver.get(self.hostname + self.url)
