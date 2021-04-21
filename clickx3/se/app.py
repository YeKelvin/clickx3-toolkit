#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from clickx3.common.exceptions import AppException
from clickx3.se.driver import Driver
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class WebApp:
    environments = None  # type: dict or str
    base_url = None  # type: str

    def __init__(self, driver: Driver, env: str = None):
        if not self.environments:
            raise AppException('environments不允许为空')

        self.driver = driver
        self.env = env
        self.__set_base_url()

    def __set_base_url(self):
        if not self.env:
            return

        if self.env and (self.env not in self.environments):
            raise AppException(f'不支持的环境名称 env:[ {self.env} ] environments:[ {self.environments} ]')

        self.base_url = self.environments.get(self.env) if isinstance(self.environments, dict) else self.environments

    def start(self):
        self.driver.get(self.base_url)

    def clear(self):
        self.driver.clear_cookies()
        self.driver.clear_local_storage()
        self.driver.clear_session_storage()

    def clear_and_refresh(self):
        self.clear()
        self.driver.refresh()
