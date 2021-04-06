#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : website.py
# @Time    : 2020/10/13 17:02
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import AppException
from appuiautomator.se.driver import Container
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class WebApp:
    env_url = None  # type: dict or str
    base_url = None  # type: str

    def __init__(self, container: Container, env: str = None):
        if not self.env_url:
            raise AppException('env_url不允许为空')

        self.__set_base_url(env)

        self.container = container
        self.env = env

    def __set_base_url(self, env):
        if not env:
            return

        if env and (env not in self.env_url):
            raise AppException(f'不支持的环境名称 env:[ {env} ] env_url:[ {self.env_url} ]')

        self.base_url = self.env_url.get(env) if isinstance(self.env_url, dict) else self.env_url

    def start(self):
        log.info('打开地址:[ {base_url} ]')
        self.container.driver.get(self.base_url)
