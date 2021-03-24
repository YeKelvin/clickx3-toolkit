#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from typing import Union

from appuiautomator.exceptions import WebSiteException
from appuiautomator.se.page import Page
from appuiautomator.se.webdriver import Browser
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class WebSite:
    hostname = None  # type:Union[dict, str, None]
    root_url = None  # type:str

    def __new__(cls, browser: Browser, env: str = None):
        if not cls.hostname:
            raise WebSiteException('WebSite hostname can not be empty')

        if env:
            if env not in cls.hostname:
                raise WebSiteException(f'The environment is not in configuration, env={env}, hostname={cls.hostname}')
            cls.root_url = cls.hostname.get(env)

        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将WebSite的driver赋值给Page
                attr.browser = browser
                attr.root_url = cls.root_url
        return super(WebSite, cls).__new__(cls)

    def __init__(self, browser: Browser, env: str = None):
        self.browser = browser
        self.env = env

    def start(self):
        self.browser.driver.get(self.root_url)
