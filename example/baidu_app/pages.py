#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pages
# @Time    : 2020/4/3 11:22
# @Author  : Kelvin.Ye
from appuiautomator.u2.page_object import PageObject, PageElement
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class HomePage(PageObject):
    """主页
    """
    search_tip = PageElement(resourceId='com.baidu.searchcraft:id/search_tip')
    search_input = PageElement(resourceId='com.baidu.searchcraft:id/toolbar_input_box_layout2')
    search_button = PageElement(resourceId='com.baidu.searchcraft:id/toolbar_btn_input_right')

    def search(self, text: str) -> None:
        """搜索
        """
        self.search_tip.click()
        self.search_input = text
        self.search_button.click()


class SearchResultPage(PageObject):
    """搜索结果列表页
    """
    head_queryarea = PageElement(resourceId='head-queryarea')

    def get_head_query_text(self):
        """获取搜索结果列表页中顶部搜索栏的文本
        """
        return self.head_queryarea.get_text()
