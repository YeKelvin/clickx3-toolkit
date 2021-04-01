#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import WebSiteException
from appuiautomator.se.page import Page
from appuiautomator.se.webdriver import Browser
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class WebApp:
    env_url = None  # type: dict or str
    base_url = None  # type: str

    def __new__(cls, browser: Browser, env: str = None):
        if not cls.env_url:
            raise WebSiteException('WebSite env_url can not be empty')

        if env:
            if env not in cls.env_url:
                raise WebSiteException(f'The environment is not in configuration, env={env}, env_url={cls.env_url}')
            cls.base_url = cls.env_url.get(env) if isinstance(cls.env_url, dict) else cls.env_url

        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将WebSite的driver赋值给Page
                attr.browser = browser
                attr.base_url = cls.base_url
        return super(WebApp, cls).__new__(cls)

    def __init__(self, browser: Browser, env: str = None):
        self.browser = browser
        self.env = env

    def start(self):
        self.browser.driver.get(self.base_url)
