#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app_object.py
# @Time    : 2020/4/3 10:47
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import AppError
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class App:
    package_name = None
    activity = None
    uri = None

    def __init__(self, device: Device):
        if not self.package_name:
            raise AppError('App Package Name can not be empty.')
        self.device = device
        self.pages = []

    def start(self):
        self.device.app_start(self.package_name, self.activity)

    def start_by_uri(self):
        """adb shell am start -a android.intent.action.VIEW -d scheme://xxx/xxx
        """
        self.device.shell(f'am start -a android.intent.action.VIEW -d {self.uri}')

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
