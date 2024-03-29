#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
from clickx3.common.exceptions import PageException
from clickx3.u2.app import AndroidApp
from clickx3.u2.device import Device
from clickx3.utils.log_util import get_logger


log = get_logger(__name__)


class Page:
    package_name = None  # type: str
    activity_name = None  # type: str
    url = None  # type: str

    def __init__(self):
        self.initialized = False  # type: bool
        self.device = None  # type: Device
        self.env = None  # type: str

    def __get__(self, instance, owner):
        if not self.initialized:
            if instance is None:
                raise PageException('持有类没有实例化')

            assert not isinstance(owner, AndroidApp)

            self.package_name = instance.package_name
            self.device = instance.device
            self.env = instance.env
            self.initialized = True

        return self

    def __set__(self, instance, value):
        raise NotImplementedError('用不着')

    def to_here(self):
        if not self.url:
            raise PageException(f'没有提供url，page:[ {self} ]')

        log.info(f'根据url打开页面，url:[ {self.url} ]')
        self.device.open_url(self.url)

    def open_activity(self):
        if (not self.package_name) or (not self.activity_name):
            raise PageException(f'没有提供package或activity，page:[ {self} ]')

        log.info(f'根据activity打开页面，activity:[ {self.activity} ]')
        self.device.app_start(self.package_name, self.activity)
