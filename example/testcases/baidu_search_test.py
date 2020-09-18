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
from appuiautomator.utils.logger import get_logger
from example.pages.baidu_search import SimpleSearchApp

log = get_logger(__name__)


class TestBaiduSearch:
    def test_search(self):
        device = Device(DevicesManager.android().get_device())
        app = SimpleSearchApp(device)
        app.restart()
        app.home_page.search('uiautomator2')


if __name__ == '__main__':
    TestBaiduSearch().test_search()
