#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import (
    PageError
)
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Page:
    def __init__(self, device=None):
        self.pages = []
        if device:
            self.device: Device = device

    def __get__(self, instance, owner):
        if instance is None:
            return None
        pages = instance.pages
        for page in pages:
            if isinstance(page, type(self)):
                return page
        self.device = instance.device
        pages.append(self)
        return self

    def __set__(self, instance, value):
        raise PageError('Can not set value')
