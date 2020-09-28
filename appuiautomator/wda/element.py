#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/18 11:17
# @Author  : Kelvin.Ye
from typing import Union

import wda

from appuiautomator.exceptions import PageElementError

LOCATORS = [
    'id',
    'name',
    'text',
    'label',
    'labelContains',
    'nameContains',
    'className',
    'visible',
    'enabled',
    'xpath',
    'predicate',
    'classChain'

]


class Element:
    @property
    def location_info(self):
        return (
            f'Location:{[k + "=" + v for k, v in self.kwargs.items()]}, Description:{str(self.description)}'
        )

    def __init__(self, timeout=5, desc='', **kwargs):
        self.timeout = timeout
        self.description = desc
        if not kwargs:
            raise ValueError('Please specify a locator.')
        self.kwargs = kwargs
        for locator, value in kwargs.items():
            if locator not in LOCATORS:
                raise KeyError(f'Element positioning of type [ {locator} ] is not supported.')

    def find(self, context) -> Union[wda.Selector, wda.Element]:
        try:
            element = context(**self.kwargs)
            element.wait(timeout=self.timeout)
            if element.exists():
                return element
            else:
                raise PageElementError()
        except (wda.WDAElementNotFoundError, PageElementError):
            raise PageElementError(f'Element not found. {self.location_info}')

    def __get__(self, instance, owner) -> Union[wda.Selector, wda.Element, None]:
        if instance is None:
            return None
        context = instance.session
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise PageElementError(f'Can not set value, no elements found. {self.location_info}')
        element.set_text(value)
