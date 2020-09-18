#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : search_result
# @Time    : 2020/9/1 16:19
# @Author  : Kelvin.Ye
from appuiautomator.u2.page import Page
from appuiautomator.u2.element import PageElement, XPathElement
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class SearchResultPage(Page):
    """搜索结果列表页
    """
    head_queryarea = PageElement(className='android.view.View', text='uiautomator2')
    # head_queryarea = PageElement(className='android.view.View', id='head-queryarea')
