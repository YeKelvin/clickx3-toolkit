#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : u2_test
# @Time    : 2020/4/2 16:14
# @Author  : Kelvin.Ye
import uiautomator2 as u2

from appuiautomator.devices_manager import DevicesManager

if __name__ == '__main__':
    serial = DevicesManager.android().get_device()
    d = u2.connect(serial)
    el = d(resourceId='')
