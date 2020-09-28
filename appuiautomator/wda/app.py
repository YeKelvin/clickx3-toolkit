#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
from typing import Optional

from appuiautomator.wda import Page


class App:
    bundle_id = ''  # type: Optional[str]

    def __new__(cls, device):
        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将App的device和session赋值给Page
                attr.device = device
                attr.session = device.session
        return super(App, cls).__new__(cls)

    def __init__(self, device):
        self.device = device
        self.session = device.session
