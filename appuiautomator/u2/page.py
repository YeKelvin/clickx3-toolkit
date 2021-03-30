#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
from typing import Optional

from appuiautomator.u2.device import Device
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class Page:
    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, value):
        if (not value) or (not isinstance(value, Device)):
            raise TypeError('不允许赋值为非Device类')

        self.__device = value
        for attr in self.__dict__.values():
            if isinstance(attr, self.__class__):
                attr.device = value

    def __init__(self, device: Optional[Device] = None):
        if device:
            self.__device: Device = device
