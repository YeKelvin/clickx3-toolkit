#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/17 21:29
# @Author  : Kelvin.Ye
import os
from datetime import datetime
from typing import List, Union

from appuiautomator.exceptions import (ElementException,
                                       ElementNotFoundException,
                                       ElementsException,
                                       XPathElementException,
                                       XPathElementsException)
from appuiautomator.utils import config
from appuiautomator.utils.log_util import get_logger
from uiautomator2 import UiObject, UiObjectNotFoundError
from uiautomator2.exceptions import XPathElementNotFoundError
from uiautomator2.xpath import XPathSelector

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
            f'Location: {[str(k) + "=" + str(v) for k, v in self.kwargs.items()]} '
            f'Description:[ {str(self.description)} ]'
        )

    def __init__(self, timeout=5, desc=None, **kwargs):
        if not kwargs:
            raise ValueError('请指定元素定位信息')
        for locator in kwargs.keys():
            if locator not in LOCATORS:
                raise KeyError(f'不支持的元素定位类型:[ {locator} ]，请输入正确的元素定位类型')
        self.timeout = timeout
        self.description = desc
        self.kwargs = kwargs

    def find(self, context) -> UiObject:
        try:
            element = context(**self.kwargs)
            element.wait(timeout=self.timeout)
            if element.exists():
                return element
            else:
                raise ElementException()
        except (UiObjectNotFoundError, ElementException):
            raise ElementNotFoundException(f'找不到元素 {self.location_info}')

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
            raise ElementException(f'赋值失败，找不到元素 {self.location_info}')
        element.set_text(value)


class Elements(Element):
    def find(self, context) -> UiObject:
        try:
            elements = context(**self.kwargs)
            elements.wait(timeout=self.timeout)
            if elements.exists():
                return elements
            else:
                raise ElementsException()
        except (UiObjectNotFoundError, ElementsException):
            raise ElementNotFoundException(f'找不到元素 {self.location_info}')

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        if elements.count == 0:
            raise ElementsException(f'赋值失败，找不到元素 {self.location_info}')
        [element.set_text(value) for element in elements]


class XPathElement:
    @property
    def location_info(self):
        return (f'Location:xpath:[ {self.xpath} ] Description:[ {str(self.description)} ]')

    def __init__(self, xpath, timeout=5, desc=''):
        if not xpath:
            raise ValueError('请指定元素xpath的定位信息')

        self.timeout = timeout
        self.description = desc
        self.xpath = xpath

    def find(self, context) -> XPathSelector:
        try:
            element = context.xpath(self.xpath)
            element.wait(timeout=self.timeout)
            if element and element.exists:
                return element
            else:
                raise XPathElementException()
        except (XPathElementNotFoundError, XPathElementException):
            raise ElementNotFoundException(f'找不到元素 {self.location_info}')

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
            raise XPathElementException(f'赋值失败，找不到元素 {self.location_info}')
        element.set_text(value)


class XPathElements(XPathElement):
    def find(self, context) -> list:
        try:
            elements = context.xpath(self.xpath)
            elements.wait(timeout=self.timeout)
            if elements.exists:
                return elements.all()
            else:
                raise XPathElementsException()
        except (XPathElementNotFoundError, XPathElementsException):
            raise ElementNotFoundException(f'找不到元素 {self.location_info}')

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        if len(elements) == 0:
            raise ElementsException(f'Cannot be set value, elements not found {self.location_info}')
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
        log.info(f'保存元素截图至:[ {destination} ]')
        return destination
