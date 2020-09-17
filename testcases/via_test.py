#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : base_test.py
# @Time    : 2020/8/26 18:27
# @Author  : Kelvin.Ye

"""
Via app测试案例
"""

from appuiautomator.se.chromedriver import webview_driver
from appuiautomator.utils.logger import get_logger
from pages.via import Via

log = get_logger(__name__)


class TestVia:
    def test_open_baidu(self, an_device):
        via = Via(an_device)
        via.start()
        via.wait()
        wd = webview_driver(an_device)
        wd.get(r'http://www.baidu.com')
        log.info(wd.title)
