#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from appuiautomator.se.webdriver import Browser
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class Page:
    uri = None

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
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value
        if self._base_url:
            for attr in self.__dict__.values():
                if isinstance(attr, self.__class__):
                    attr.base_url = value

    def __init__(self, browser=None, base_url=None):
        if browser:
            self._browser = browser
        if base_url:
            self._base_url = base_url

    def get(self):
        if self.base_url and self.url:
            self.browser.driver.get(self.base_url + self.url)
