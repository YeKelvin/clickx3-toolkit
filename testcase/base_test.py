#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : base_test.py
# @Time    : 2019/10/15 17:34
# @Author  : Kelvin.Ye
from appuiautomator.android import AndroidDevice
from appuiautomator.manager import AndroidDevicesManager
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class BasePyTest:
    """PyTest测试基类
    """
    dm = None
    serial = None
    device = None

    def setup_class(self):
        if self.dm is None:
            self.dm = AndroidDevicesManager()
            self.serial = self.dm.get_device()
            self.device = AndroidDevice(self.serial)

    def teardown_class(self):
        if self.dm and self.device:
            self.dm.release_device(self.serial)

    def setup_method(self):
        pass

    def teardown_method(self):
        pass
