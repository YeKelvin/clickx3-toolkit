#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from clickx3.exceptions import PageException
from clickx3.se.app import WebApp
from clickx3.se.driver import Driver
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class Page:
    uri = None

    def __init__(self):
        self.initialized = False
        self.driver = None  # type:Driver
        self.base_url = None

    def __get__(self, instance, owner):
        if not self.initialized:
            if instance is None:
                raise PageException('持有类没有实例化')

            assert not isinstance(owner, WebApp)

            self.driver = instance.driver
            self.base_url = instance.base_url
            self.env = instance.env
            self.initialized = True

        return self

    def __set__(self, instance, value):
        raise NotImplementedError('用不着')

    def to_here(self):
        if self.base_url and self.uri:
            url = self.base_url + self.uri
            self.driver.get(url)

    def wait_to_here(self, timeout=5, message=''):
        self.driver.wait.url_contains(self.uri, timeout, message)
