#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pages.py
# @Time    : 2019/9/3 10:38
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator import MobileDevice
from appuiautomator.element import By
from appuiautomator.utils.logger import get_logger
from page import BasePage

log = get_logger(__name__)


class SimpleSearchApp:
    """简单搜索app
    """
    package_name = 'com.baidu.searchcraft'
    bundle_identifier = ''

    def __init__(self, d: MobileDevice) -> None:
        self.home_page = HomePage(d)
        self.search_result_page = SearchResultPage(d)


class HomePage(BasePage):
    """主页
    """
    _android_elements = {
        'search_tip': {By.resourceId: 'com.baidu.searchcraft:id/search_tip'},
        'search_input_box': {By.resourceId: 'com.baidu.searchcraft:id/toolbar_input_box'},
        'search_button': {By.resourceId: 'com.baidu.searchcraft:id/toolbar_btn_input_right'}
    }

    _ios_elements = {}

    def search(self, text: str) -> None:
        """搜索
        """
        self.elements.get('search_tip').click()
        self.elements.get('search_input_box').set_text(text)
        self.elements.get('search_button').click()


class SearchResultPage(BasePage):
    """搜索结果列表页
    """
    _android_elements = {
        'head_queryarea': {By.resourceId: 'head-queryarea'}
    }

    _ios_elements = {}

    def get_head_query_text(self):
        """获取搜索结果列表页中顶部搜索栏的文本
        """
        return self.elements.get('head_queryarea').get_text()
