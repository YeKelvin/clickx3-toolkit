#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : base_test.py
# @Time    : 2019/10/15 17:34
# @Author  : Kelvin.Ye
import uiautomator2 as u2
from appuiautomator.devices_manager import AndroidDevicesManager
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class AndroidCase:
    """Android设备 PyTest测试基类
    """
    serial = None
    device = None

    def setup_class(self):
        self.serial = AndroidDevicesManager().get_device()
        self.device = Device(u2.connect(self.serial))

    def teardown_class(self):
        if self.device:
            AndroidDevicesManager().release_device(self.serial)

    def setup_method(self):
        pass

    def teardown_method(self):
        pass


class IosCase:
    """IOS设备 PyTest测试基类
    """
