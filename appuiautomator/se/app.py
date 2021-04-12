#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import AppException
from appuiautomator.se.driver import Driver
from appuiautomator.utils.log_util import get_logger
from selenium.webdriver.remote.webdriver import WebDriver

log = get_logger(__name__)


class WebApp:
    environments = None  # type: dict or str
    base_url = None  # type: str

    def __init__(self, driver: Driver, env: str = None):
        if not self.environments:
            raise AppException('environments不允许为空')

        self.__set_base_url(env)
        self.driver = driver  # type: WebDriver

    def __set_base_url(self, env):
        if not env:
            return

        if env and (env not in self.environments):
            raise AppException(f'不支持的环境名称 env:[ {env} ] environments:[ {self.environments} ]')

        self.base_url = self.environments.get(env) if isinstance(self.environments, dict) else self.environments

    def start(self):
        log.info(f'打开地址:[ {self.base_url} ]')
        self.driver.get(self.base_url)
