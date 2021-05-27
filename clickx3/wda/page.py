#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/2 17:47
# @Author  : Kelvin.Ye
from clickx3.common.exceptions import PageException
from clickx3.utils.log_util import get_logger
from clickx3.wda.app import IOSApp
from clickx3.wda.device import Device


log = get_logger(__name__)


class Page:

    def __init__(self):
        self.initialized = False  # type: bool
        self.device = None  # type: Device
        self.env = None  # type: str

    def __get__(self, instance, owner):
        if not self.initialized:
            if instance is None:
                raise PageException('持有类没有实例化')

            assert not isinstance(owner, IOSApp)

            self.device = instance.device
            self.env = instance.env
            self.initialized = True

        return self

    def __set__(self, instance, value):
        raise NotImplementedError('用不着')
