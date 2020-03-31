#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : demo_test.py
# @Time    : 2019/9/3 10:38
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from core import MobileDevice
from core.utils.logger import get_logger
from examples.baidu_pages import SimpleSearchApp

log = get_logger(__name__)


class BaiduTest:
    def test_search(self):
        d = MobileDevice('GSLDU16823001086')
        d.app.stop(SimpleSearchApp.package_name)
        d.app.start(SimpleSearchApp.package_name)
        app = SimpleSearchApp(d)
        app.home_page.search('uiautomator2')
        assert app.search_result_page.get_head_query_text() == 'uiautomator2'


if __name__ == '__main__':
    BaiduTest().test_search()
