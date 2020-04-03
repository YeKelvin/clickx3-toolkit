#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pages
# @Time    : 2020/4/3 18:28
# @Author  : Kelvin.Ye
from appuiautomator.u2.page import Page, PageElement, XPathElement
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class HomePage(Page):
    """主页
    """
    search_tip = PageElement(resourceId='com.baidu.searchcraft:id/search_tip')
    search_input = PageElement(resourceId='com.baidu.searchcraft:id/toolbar_input_box_layout2')
    search_button = PageElement(resourceId='com.baidu.searchcraft:id/toolbar_btn_input_right')

    def search(self, text: str) -> None:
        """搜索
        """
        self.search_tip.click()
        self.device.fastinput_ime(text)
        self.search_button.click()


class SearchResultPage(Page):
    """搜索结果列表页
    """
    head_queryarea = PageElement(className='android.view.View', text='uiautomator2')
    # head_queryarea = PageElement(className='android.view.View', id='head-queryarea')
