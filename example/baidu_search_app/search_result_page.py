#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : search_result_page
# @Time    : 2020/4/3 14:43
# @Author  : Kelvin.Ye
from appuiautomator.u2.page_object import PageObject, PageElement
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class SearchResultPage(PageObject):
    """搜索结果列表页
    """
    head_queryarea = PageElement(resourceId='head-queryarea')

    def get_head_query_text(self):
        """获取搜索结果列表页中顶部搜索栏的文本
        """
        return self.head_queryarea.get_text()
