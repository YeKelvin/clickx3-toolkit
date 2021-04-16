#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : chrome_test
# @Time    : 2020/9/17 15:14
# @Author  : Kelvin.Ye

"""
Chrome app测试案例
"""
import pytest

from clickx3.se.support.chromedriver import webview_driver
from clickx3.utils.log_util import get_logger
from pages.chrome.android import Chrome

log = get_logger(__name__)

pytestmark = [pytest.mark.h5test]


class TestChrome:
    def test_open_baidu(self, an_device):
        chrome = Chrome(an_device)
        chrome.start()
        chrome.wait()
        wd = webview_driver(an_device)
        wd.get(r'http://www.baidu.com')
        log.info(wd.title)
