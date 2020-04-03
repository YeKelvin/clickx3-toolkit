#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2020/4/3 11:22
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator.u2.app_object import AppObject, Page
from appuiautomator.utils.logger import get_logger
from example.baidu_app.pages import HomePage, SearchResultPage

log = get_logger(__name__)


class SimpleSearchApp(AppObject):
    """简单搜索app
    """
    package_name = 'com.baidu.searchcraft'
    bundle_identifier = ''

    home_page = Page(HomePage)
    search_result_page = Page(SearchResultPage)
