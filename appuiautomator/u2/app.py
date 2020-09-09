#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app_object.py
# @Time    : 2020/4/3 10:47
# @Author  : Kelvin.Ye
import uiautomator2 as u2

from appuiautomator.exceptions import AppError
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class App:
    package_name = None
    uri = None

    def __init__(self, device):
        if not self.package_name:
            raise AppError('App Package Name can not be empty.')
        self.device: Device = device
        self.driver: u2.Device = device.driver
        self.pages: list = []

    def start(self):
        self.device.app_start(self.package_name)

    def start_by_uri(self):
        """adb shell am start -a android.intent.action.VIEW -d scheme://xxx/xxx
        """
        self.device.run_adb_shell(f'am start -a android.intent.action.VIEW -d {self.uri}')

    def stop(self):
        self.device.app_stop(self.package_name)

    def wait(self):
        self.device.app_wait(self.package_name)

    def clear(self):
        self.device.app_clear(self.package_name)

    def restart(self):
        self.stop()
        self.start()
        self.wait()
