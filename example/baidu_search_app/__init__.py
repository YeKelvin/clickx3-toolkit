#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2020/4/3 11:22
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator.u2.app import App
from appuiautomator.utils.logger import get_logger
from example.baidu_search_app.pages import HomePage, SearchResultPage

log = get_logger(__name__)


class SimpleSearchApp(App):
    """简单搜索app
    """
    package_name = 'com.baidu.searchcraft'
    bundle_identifier = ''

    home_page = HomePage()
    search_result_page = SearchResultPage()
