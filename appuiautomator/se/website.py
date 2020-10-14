#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import WebSiteException
from appuiautomator.se.page import Page
from appuiautomator.se.webdriver import Browser
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class WebSite:
    hostname = None

    def __new__(cls, browser: Browser):
        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将WebSite的driver赋值给Page
                attr.browser = browser
                attr.hostname = cls.hostname
        return super(WebSite, cls).__new__(cls)

    def __init__(self, browser: Browser):
        if not self.hostname:
            raise WebSiteException('WebSite hostname can not be empty')
        self.browser = browser

    def start(self):
        self.browser.driver.get(self.hostname)
