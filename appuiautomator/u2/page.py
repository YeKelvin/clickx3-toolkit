#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
from typing import Optional

from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Page:
    def __init__(self, device: Optional[Device] = None):
        if device:
            self.device: Device = device

    # def __get__(self, instance, owner):
    #     """
    #
    #     Args:
    #         instance:   appuiautomator.u2.app.App类实例
    #         owner:      appuiautomator.u2.app.App类
    #
    #     Returns:        self
    #
    #     """
    #     device = getattr(instance, 'device', None)
    #
    #     if device:
    #         self.device = instance.device  # 将App对象的device属性传递给Page对象
    #     return self
    #
    # def __set__(self, instance, value):
    #     raise PageError('Can not set value')
