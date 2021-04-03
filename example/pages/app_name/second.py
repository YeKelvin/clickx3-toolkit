#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : search_result
# @Time    : 2020/9/1 16:19
# @Author  : Kelvin.Ye
from appuiautomator.u2.page import Page
from appuiautomator.u2.element import Element
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class SecondPage(Page):

    xxx_input = Element(resourceId='xxx.xxx.xxx')
    xxx_btn = Element(resourceId='xxx.xxx.xxx')
    xxx_txt = Element(resourceId='xxx.xxx.xxx')

    def do_something(self):
        ...
