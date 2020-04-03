#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
import os
import uiautomator2 as u2
from datetime import datetime
from typing import Union

from uiautomator2 import UiObjectNotFoundError
from uiautomator2.exceptions import XPathElementNotFoundError
from uiautomator2.session import UiObject
from uiautomator2.xpath import XPathSelector

from appuiautomator.exceptions import PageElementError, PageElementsError, XPathElementsError, XPathElementError
from appuiautomator.u2.device import Device
from appuiautomator.utils import config
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

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
    'innerElement': 'innerElement',
    'allowScrollSearch': 'allow_scroll_search'
}


class PageObject:
    def __init__(self, device):
        self.device: Device = device
        self.driver: u2.Device = device.driver


class PageElement:
    @property
    def location_info(self):
        return [k + "=" + v for k, v in self.kwargs.items()]

    def __init__(self, timeout=5, desc='', **kwargs):
        self.timeout = timeout
        self.description = desc
        if not kwargs:
            raise ValueError('Please specify a locator.')
        self.kwargs = kwargs
        for locator, value in kwargs.items():
            if locator not in LOCATORS:
                raise KeyError(f'Element positioning of type [ {locator} ] is not supported.')

    def find(self, context) -> UiObject:
        try:
            element = context(**self.kwargs)
            element.wait(timeout=self.timeout)
            if element.exists():
                return element
            else:
                raise PageElementError()
        except (UiObjectNotFoundError, PageElementError):
            raise PageElementError(
                f'Element not found. Location:{self.location_info} Description:{self.description}'
            )

    def __get__(self, instance, owner) -> Union[UiObject, list, None]:
        if instance is None:
            return None
        context = instance.driver
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise PageElementError(
                f'Can not set value, no elements found. Location:{self.location_info} Description:{self.description}'
            )
        element.set_text(value)


class PageElements(PageElement):
    def find(self, context) -> Union[UiObject]:
        try:
            elements = context(**self.kwargs)
            elements.wait(timeout=self.timeout)
            if elements.exists():
                return elements
            else:
                raise PageElementsError()
        except (UiObjectNotFoundError, PageElementsError):
            raise PageElementsError(
                f'Element not found. Location:{self.location_info} Description:{self.description}'
            )

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        if elements.count == 0:
            raise PageElementsError(
                f'Can not set value, no elements found. Location:{self.location_info} Description:{self.description}'
            )
        [element.set_text(value) for element in elements]


class XPathElement:
    def __init__(self, xpath, timeout=5, desc=''):
        self.timeout = timeout
        self.description = desc
        if not xpath:
            raise ValueError('Please specify a xpath locator.')
        self.xpath = xpath

    def find(self, context) -> XPathSelector:
        try:
            element = context.xpath(self.xpath)
            element.wait(timeout=self.timeout)
            if element and element.exists:
                return element
            else:
                raise XPathElementError()
        except (XPathElementNotFoundError, XPathElementError):
            raise XPathElementError(
                f'Element not found. Location:xpath={self.xpath} Description:{self.description}'
            )

    def __get__(self, instance, owner) -> Union[XPathSelector, list, None]:
        if instance is None:
            return None
        context = instance.driver
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise XPathElementError(
                f'Can not set value, no elements found. Location:xpath={self.xpath} Description:{self.description}'
            )
        element.set_text(value)


class XPathElements(XPathElement):
    def find(self, context) -> list:
        try:
            elements = context.xpath(self.xpath)
            elements.wait(timeout=self.timeout)
            if elements.exists:
                return elements.all()
            else:
                raise XPathElementsError()
        except (XPathElementNotFoundError, XPathElementsError):
            raise XPathElementsError(
                f'Element not found. Location:xpath={self.xpath} Description:{self.description}'
            )

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        if len(elements) == 0:
            raise PageElementsError(
                f'Can not set value, no elements found. Location:xpath={self.xpath} Description:{self.description}'
            )
        [element.set_text(value) for element in elements]


class ElementUtil:
    @staticmethod
    def screenshot_by_element(driver, element, destination: str = None) -> str:
        """元素级截图
        """
        element_info = element.info
        bounds = element_info.info.get('bounds')
        left = bounds.get('left')
        top = bounds.get('top')
        right = bounds.get('right')
        bottom = bounds.get('bottom')
        # 设备截图
        image = driver.screenshot()
        # 截图剪裁
        cropped = image.crop((left, top, right, bottom))
        if not destination:
            destination = os.path.join(
                config.get_project_path(),
                'testcase', '.tmp',
                f'{datetime.now().strftime("%Y%m%d.%H%M%S.%f")}.jpg'
            )
        cropped.save(destination)
        log.info(f'保存元素截图至 {destination}')
        return destination
