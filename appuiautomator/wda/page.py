#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/2 17:47
# @Author  : Kelvin.Ye
from appuiautomator.wda.app import IOSApp
from appuiautomator.wda.device import Device
from appuiautomator.utils.log_util import get_logger
from appuiautomator.exceptions import PageException

log = get_logger(__name__)


class Page:
    def __init__(self):
        self.initialized = False
        self.device: Device = None

    def __get__(self, instance, owner):
        if not self.initialized:
            if instance is None:
                raise PageException('持有类没有实例化')

            assert not isinstance(owner, IOSApp)

            self.client = instance.client
            self.initialized = True

        return self

    def __set__(self, instance, value):
        raise NotImplementedError('用不着')
