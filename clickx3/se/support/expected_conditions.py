#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : expected_conditions.py
# @Time    : 2021/4/15 13:06
# @Author  : Kelvin.Ye


class clickable_of:
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return self.element.is_enabled()


class image_completed_of:
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return bool(self.element.get_attribute('complete'))


class text_contains_of:
    def __init__(self, element, expected, refresh=False):
        self.element = element
        self.expected = expected
        self.refresh = refresh

    def __call__(self, driver):
        if self.refresh:
            driver.refresh()
        return self.expected in self.element.text
