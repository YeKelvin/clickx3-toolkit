#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : demo_test.py
# @Time    : 2019/9/3 10:38
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator.devices_manager import DevicesManager
from appuiautomator.u2.device import Device
from appuiautomator.utils.log_util import get_logger
from example.pages.app_name import ApplicationName

log = get_logger(__name__)


class TestApplicationName:
    def test_search(self):
        device = Device(DevicesManager.android().get_device())
        app = ApplicationName(device)
        app.action.do_action()