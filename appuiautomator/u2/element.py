#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/17 21:29
# @Author  : Kelvin.Ye
import os
from datetime import datetime
from typing import Union, List

from uiautomator2 import UiObjectNotFoundError
from uiautomator2.exceptions import XPathElementNotFoundError
from uiautomator2.session import UiObject
from uiautomator2.xpath import XPathSelector

from appuiautomator.exceptions import PageElementError, PageElementsError, XPathElementsError, XPathElementError
from appuiautomator.utils import config
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

LOCATORS = [
    'text',
    'textContains',
    'textMatches',
    'textStartsWith',
    'className',
    'classNameMatches',
    'description',
    'descriptionContains',
    'descriptionMatches',
    'descriptionStartsWit',
    'checkable',
    'checked',
    'clickable',
    'longClickable',
    'scrollable',
    'enabled',
    'focusable',
    'focused',
    'selected',
    'packageName',
    'packageNameMatches',
    'resourceId',
    'resourceIdMatches',
    'index',
    'instance',
    'innerElement',
    'allowScrollSearch'
]


class Element:
    @property
    def location_info(self):
        return (
            f'Location:{[str(k) + "=" + str(v) for k, v in self.kwargs.items()]}, Description:{str(self.description)}'
        )

    def __init__(self, timeout=5, desc=None, **kwargs):
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
            raise PageElementError(f'Element not found. {self.location_info}')

    def __get__(self, instance, owner) -> Union[UiObject, List[UiObject], None]:
        """

        :param instance:    appuiautomator.u2.page.Page类实例
        :param owner:       appuiautomator.u2.page.Page类
        :return:
        """
        if instance is None:
            return None
        context = instance.device  # 将Page对象的device属性传递给PageElement对象
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise PageElementError(f'Can not set value, no elements found. {self.location_info}')
        element.set_text(value)


class Elements(Element):
    def find(self, context) -> UiObject:
        try:
            elements = context(**self.kwargs)
            elements.wait(timeout=self.timeout)
            if elements.exists():
                return elements
            else:
                raise PageElementsError()
        except (UiObjectNotFoundError, PageElementsError):
            raise PageElementsError(f'Element not found. {self.location_info}')

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        if elements.count == 0:
            raise PageElementsError(f'Can not set value, no elements found. {self.location_info}')
        [element.set_text(value) for element in elements]


class XPathElement:
    @property
    def location_info(self):
        return (
            f'Location:xpath={self.xpath}, Description:{str(self.description)}'
        )

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
            raise XPathElementError(f'Element not found. {self.location_info}')

    def __get__(self, instance, owner) -> Union[XPathSelector, List[XPathSelector], None]:
        """

        Args:
            instance:   appuiautomator.u2.page.Page类实例
            owner:      appuiautomator.u2.page.Page类

        Returns:

        """
        if instance is None:
            return None
        context = instance.device  # 将Page对象的device属性传递给PageElement对象
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise XPathElementError(f'Can not set value, no elements found. {self.location_info}')
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
            raise XPathElementsError(f'Element not found. {self.location_info}')

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        if len(elements) == 0:
            raise PageElementsError(f'Can not set value, no elements found. {self.location_info}')
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
                config.project_path(),
                'testcase', '.tmp',
                f'{datetime.now().strftime("%Y%m%d.%H%M%S.%f")}.jpg'
            )
        cropped.save(destination)
        log.info(f'保存元素截图至 {destination}')
        return destination
