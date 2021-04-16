#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : expected_conditions.py
# @Time    : 2021/4/15 13:06
# @Author  : Kelvin.Ye

# Not yet implemented
# from uiautomator2 import UiObject as U2Element
# from uiautomator2.xpath import XMLElement as U2XMLElement
# from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError


class text_contains_of_element:
    def __init__(self, element, text):
        self.target = element
        self.expected = text

    def __call__(self, device):
        return self.target.get_text().contains(self.expected)
