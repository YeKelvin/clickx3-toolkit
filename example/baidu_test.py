#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : demo_test.py
# @Time    : 2019/9/3 10:38
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""
import uiautomator2 as u2
from appuiautomator.utils.logger import get_logger
from example.baidu_pages import SimpleSearchApp, HomePage, SearchResultPage

log = get_logger(__name__)


class TestBaidu:
    def test_search(self):
        d = u2.connect('GSLDU16823001086')
        app = SimpleSearchApp(d)
        app.app_stop(app.package_name)
        app.app_start(app.package_name)
        app.app_wait(app.package_name)
        home_page = HomePage(d)
        home_page.search('uiautomator2')


if __name__ == '__main__':
    TestBaidu().test_search()
