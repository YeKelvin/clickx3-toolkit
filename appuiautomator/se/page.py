#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from appuiautomator.se.webdriver import Browser
from appuiautomator.utils.log_util import get_logger

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
    def root_url(self):
        return self._root_url

    @root_url.setter
    def root_url(self, value):
        self._root_url = value
        if self._root_url:
            for attr in self.__dict__.values():
                if isinstance(attr, self.__class__):
                    attr.root_url = value

    def __init__(self, browser=None, root_url=None):
        if browser:
            self._browser = browser
        if root_url:
            self._root_url = root_url

    def get(self):
        if self.root_url and self.url:
            self.browser.driver.get(self.root_url + self.url)
