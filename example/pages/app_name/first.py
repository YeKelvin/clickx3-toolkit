#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : home
# @Time    : 2020/9/1 16:17
# @Author  : Kelvin.Ye
from clickx3.u2.element import Element
from clickx3.u2.page import Page
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class FirstPage(Page):

    xxx_input = Element(resourceId='xxx.xxx.xxx')
    xxx_btn = Element(resourceId='xxx.xxx.xxx')
    xxx_txt = Element(resourceId='xxx.xxx.xxx')

    def do_something(self):
        ...
