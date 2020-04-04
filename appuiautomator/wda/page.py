#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : wda_po
# @Time    : 2020/4/2 17:47
# @Author  : Kelvin.Ye
from typing import Union

import wda

from appuiautomator.exceptions import PageError, PageElementError
from appuiautomator.wda.device import Device

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


class Page:
    def __init__(self, device=None):
        self.pages = []
        if device:
            self.device: Device = device
            self.session: wda.Client = device.sesson

    def __get__(self, instance, owner):
        if instance is None:
            return None
        pages = instance.pages
        for page in pages:
            if isinstance(page, type(self)):
                return page
        self.device = instance.device
        self.session = instance.device.session
        pages.append(self)
        return self

    def __set__(self, instance, value):
        raise PageError('Can not set value')


class PageElement:
    @property
    def location_info(self):
        return (
            f'Location:{[k + "=" + v for k, v in self.kwargs.items()]} '
            f'{"Description:" + self.description if self.description else ""}'
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
