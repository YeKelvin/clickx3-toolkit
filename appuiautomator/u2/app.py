#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app_object.py
# @Time    : 2020/4/3 10:47
# @Author  : Kelvin.Ye
from typing import Optional

from appuiautomator.exceptions import AppException
from appuiautomator.u2.device import Device
from appuiautomator.u2.page import Page
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class App:
    package_name = None  # type: Optional[str]
    activity = None  # type: Optional[str]
    uri = None  # type: Optional[str]

    def __new__(cls, device: Device):
        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将App的device赋值给Page
                attr.device = device
        return super(App, cls).__new__(cls)

    def __init__(self, device: Device):
        if not self.package_name:
            raise AppException('App Package Name cannot be empty')
        self.device = device

    def start(self):
        self.device.app_start(self.package_name, self.activity)

    def start_by_uri(self):
        self.device.activity_start_by_uri(self.uri)

    def stop(self):
        self.device.app_stop(self.package_name)

    def wait(self):
        self.device.app_wait(self.package_name)

    def clear(self):
        self.device.app_clear(self.package_name)

    def clear_and_start(self):
        self.clear()
        self.start()
        self.wait()

    def restart(self):
        self.stop()
        self.start()
        self.wait()
