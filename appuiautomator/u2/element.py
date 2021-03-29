#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/17 21:29
# @Author  : Kelvin.Ye
import os
from datetime import datetime
from time import sleep
from typing import List, Union

from appuiautomator.exceptions import ElementsException, XPathElementException
from appuiautomator.u2.device import Device
from appuiautomator.utils import config
from appuiautomator.utils.log_util import get_logger
from uiautomator2 import UiObject, UiObjectNotFoundError
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


class Element(UiObject):
    def __init__(self, ui_obj: UiObject = None,
                 delay=0.5, timeout=10, interval=0.5, **kwargs):
        if ui_obj:
            # 直接把UiObject的属性字典复制过来
            self.__dict__ = ui_obj.__dict__

        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.kwargs = kwargs

    def __find(self, device: Device):
        # 计算重试次数
        retry_count = int(int(self.timeout) / int(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = device(**self.kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
            else:
                raise UiObjectNotFoundError(str(element.selector))

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            element = device(**self.kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
        raise UiObjectNotFoundError(str(element.selector))

    def __get__(self, instance, owner):
        """

        :param instance:    持有该类的父类实例（appuiautomator.u2.page.Page）
        :param owner:       持有该类的父类实例（appuiautomator.u2.page.Page）
        :return:
        """
        if instance is None:
            return
        return self.__find(instance.device)  # 将Page对象的device属性传递给PageElement对象

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if element:
            element.set_text(value)


class Elements(Element):
    def __find(self, context) -> UiObject:
        if self.delay:
            sleep(self.delay)
        elements = context(**self.kwargs)
        elements.must_wait(timeout=self.timeout)  # timeout后找不到元素会直接抛异常UiObjectNotFoundError
        return elements

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        # if elements.count == 0:
        #     raise ElementsException(f'赋值失败，找不到元素 {self.location_info}')
        [element.set_text(value) for element in elements]


class XPathElement:
    @property
    def location_info(self):
        return (f'Location:xpath:[ {self.xpath} ] Description:[ {str(self.description)} ]')

    def __init__(self, xpath, delay=0.5, timeout=5, desc=''):
        if not xpath:
            raise ValueError('请指定元素xpath的定位信息')

        self.delay = delay
        self.timeout = timeout
        self.description = desc
        self.xpath = xpath

    def find(self, context) -> XPathSelector:
        if self.delay:
            sleep(self.delay)
        element = context.xpath(self.xpath)
        element.must_wait(timeout=self.timeout)  # timeout后找不到元素会直接抛异常UiObjectNotFoundError
        return element

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
        if self.delay:
            sleep(self.delay)
        elements = context.xpath(self.xpath)
        elements.must_wait(timeout=self.timeout)  # timeout后找不到元素会直接抛异常UiObjectNotFoundError
        return elements.all()

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
