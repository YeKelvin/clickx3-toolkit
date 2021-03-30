#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/2 17:47
# @Author  : Kelvin.Ye
from appuiautomator.wda.device import Device
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class Page:
    def __init__(self, device=None):
        if device:
            self.device: Device = device
