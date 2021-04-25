#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : expected_conditions.py
# @Time    : 2021/4/15 13:06
# @Author  : Kelvin.Ye


class text_contains_of:

    def __init__(self, element, expected):
        self.element = element
        self.expected = expected

    def __call__(self, device):
        return self.expected in self.element.get_text()
