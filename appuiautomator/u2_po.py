#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : u2_po.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
from typing import Union

from uiautomator2.session import UiObject

from appuiautomator.exceptions import PageElementError

LOCATORS = {
    'text': 'text',
    'textContains': 'textContains',
    'textMatches': 'textMatches',
    'textStartsWith': 'textStartsWith',
    'className': 'className',
    'classNameMatches': 'classNameMatches',
    'description': 'description',
    'descriptionContains': 'descriptionContains',
    'descriptionMatches': 'descriptionMatches',
    'descriptionStartsWit': 'descriptionStartsWit',
    'checkable': 'checkable',
    'checked': 'checked',
    'clickable': 'clickable',
    'longClickable': 'longClickable',
    'scrollable': 'scrollable',
    'enabled': 'enabled',
    'focusable': 'focusable',
    'focused': 'focused',
    'selected': 'selected',
    'packageName': 'packageName',
    'packageNameMatches': 'packageNameMatches',
    'resourceId': 'resourceId',
    'resourceIdMatches': 'resourceIdMatches',
    'index': 'index',
    'instance': 'instance',
    'xpath': 'xpath',
    'innerElement': 'innerElement',
    'allowScrollSearch': 'allow_scroll_search'
}


class PageElement:

    def __init__(self, timeout=5, desc=None, **kwargs):
        self.timeout = timeout
        self.description = desc
        if not kwargs:
            raise ValueError('Please specify a locator')
        self.kwargs = kwargs
        for locator, value in kwargs.items():
            if locator not in LOCATORS:
                raise KeyError(f'Element positioning of type {locator} is not supported.')

    def get_element(self, context) -> Union[UiObject]:
        return context(**self.kwargs)

    def find(self, context) -> Union[UiObject]:
        element = self.get_element(context)
        if element.exists(timeout=self.timeout):
            return element
        else:
            raise PageElementError()

    def __get__(self, instance, owner) -> Union[UiObject, None]:
        if instance is None:
            return None
        context = instance.driver
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise PageElementError("Can't set value, element not found")
        element.set_text(value)
