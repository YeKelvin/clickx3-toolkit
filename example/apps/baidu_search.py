#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : baidu_search
# @Time    : 2020/8/27 20:16
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator.u2.app import App
from appuiautomator.utils.logger import get_logger
from example.pages.baidu_search import HomePage, SearchResultPage

log = get_logger(__name__)


class SimpleSearchApp(App):
    """简单搜索app
    """
    package_name = 'com.baidu.searchcraft'

    home_page = HomePage()
    search_result_page = SearchResultPage()
