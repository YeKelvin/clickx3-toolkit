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
