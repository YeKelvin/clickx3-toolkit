#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : wda_po
# @Time    : 2020/4/2 17:47
# @Author  : Kelvin.Ye
import wda

from appuiautomator.wda.device import Device


class Page:
    def __init__(self, device=None):
        if device:
            self.device: Device = device
            self.session: wda.Client = device.sesson

    # def __get__(self, instance, owner):
    #     if instance is None:
    #         return None
    #     self.device = instance.device
    #     self.session = instance.device.session
    #     return self
    #
    # def __set__(self, instance, value):
    #     raise PageError('Can not set value')
