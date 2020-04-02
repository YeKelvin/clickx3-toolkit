#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pages.py
# @Time    : 2019/9/3 10:38
# @Author  : Kelvin.Ye

"""
简单搜索app demo
"""

from appuiautomator.u2_po import Page, PageElement
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class SimpleSearchApp:
    """简单搜索app
    """
    package_name = 'com.baidu.searchcraft'
    bundle_identifier = ''


class HomePage(Page):
    """主页
    """
    search_tip = PageElement(resourceId='com.baidu.searchcraft:id/search_tip')
    search_input = PageElement(resourceId='com.baidu.searchcraft:id/toolbar_input_box')
    search_button = PageElement(resourceId='com.baidu.searchcraft:id/toolbar_btn_input_right')

    def search(self, text: str) -> None:
        """搜索
        """
        self.search_tip.click()
        self.search_input = text
        self.search_button.click()


class SearchResultPage(Page):
    """搜索结果列表页
    """
    head_queryarea = PageElement(resourceId='head-queryarea')

    def get_head_query_text(self):
        """获取搜索结果列表页中顶部搜索栏的文本
        """
        return self.head_queryarea.get_text()
