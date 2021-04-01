#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2020/9/1 16:16
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator.action import BaseAction
from appuiautomator.u2.app import App
from appuiautomator.utils.log_util import get_logger
from example.pages.baidu_search.home import HomePage
from example.pages.baidu_search.search_result import SearchResultPage

log = get_logger(__name__)


class Action(BaseAction):
    def __init__(self, source: 'SimpleSearch'):
        self.source = source


class SimpleSearch(App):
    """简单搜索app
    """
    package_name = 'com.baidu.searchcraft'

    home_page = HomePage()
    search_result_page = SearchResultPage()
