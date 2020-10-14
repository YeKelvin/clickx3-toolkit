#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import WebSiteException
from appuiautomator.se.page import Page
from appuiautomator.utils.logger import get_logger
from selenium.webdriver.remote.webdriver import WebDriver

log = get_logger(__name__)


class WebSite:
    hostname = None

    def __new__(cls, driver: WebDriver):
        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将WebSite的driver赋值给Page
                attr.driver = driver
                attr.hostname = cls.hostname
        return super(WebSite, cls).__new__(cls)

    def __init__(self, driver: WebDriver):
        if not self.hostname:
            raise WebSiteException('WebSite hostname can not be empty')
        self.driver = driver

    def start(self):
        self.driver.get(self.hostname)
