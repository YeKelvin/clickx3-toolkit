#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : demo_test.py
# @Time    : 2019/9/3 10:38
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

import uiautomator2 as u2

from appuiautomator.devices_manager import AndroidDevicesManager
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger
from example.pages.baidu_search import SimpleSearchApp

log = get_logger(__name__)


class TestBaiduSearch:
    def test_search(self):
        d = u2.connect(AndroidDevicesManager().get_device())
        device = Device(d)
        app = SimpleSearchApp(device)
        app.restart()
        app.home_page.search('uiautomator2')


if __name__ == '__main__':
    TestBaiduSearch().test_search()
