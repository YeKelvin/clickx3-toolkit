#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : home
# @Time    : 2020/9/1 16:40
# @Author  : Kelvin.Ye
from appuiautomator.u2.element import Element
from appuiautomator.u2.page import Page
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class HomePage(Page):
    """首页
    """
    search_input = Element(resourceId='mark.via:id/n')

    def search(self, keywords):
        self.search_input.click()
        self.search_input.set_text(keywords)
