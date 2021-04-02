#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/17 21:29
# @Author  : Kelvin.Ye
from functools import wraps
from time import sleep

from appuiautomator.exceptions import ElementException
from appuiautomator.u2.device import Device
from appuiautomator.utils.log_util import get_logger
from uiautomator2 import UiObject
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError
from uiautomator2.xpath import XPathSelector

log = get_logger(__name__)


class Locator(dict):
    ...


def _retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)
        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = func(*args, **kwargs)
            if element.exists:
                return Element(ui_object=element)
            else:
                raise UiObjectNotFoundError({'code': -32002, 'data': str(element.selector), 'method': '_retry'})
        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            element = func(*args, **kwargs)
            if element.exists:
                return Element(ui_object=element)
        raise UiObjectNotFoundError({'code': -32002, 'data': str(element.selector), 'method': '_retry'})
    return wrapper


class Element(UiObject):
    def __init__(self,
                 ui_object: UiObject = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5,
                 **kwargs):
        if ui_object:
            # 直接把UiObject的属性字典复制过来
            self.__dict__.update(ui_object.__dict__)
        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.kwargs = kwargs

    def __find(self, device: Device):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
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
                raise UiObjectNotFoundError({'code': -32002, 'data': str(element.selector), 'method': '__find'})

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            element = device(**self.kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
        raise UiObjectNotFoundError({'code': -32002, 'data': str(element.selector), 'method': '__find'})

    def scroll_to_child(self, **kwargs):
        """滚动查找元素"""
        if self.scroll.to(**kwargs):
            return self.child(**kwargs)
        else:
            raise UiObjectNotFoundError({'code': -32002, 'data': str(self.selector), 'method': 'scroll_to_child'})

    @_retry
    def child(self, **kwargs):
        return super().child(**kwargs)

    @_retry
    def sibling(self, **kwargs):
        return super().sibling(**kwargs)

    @_retry
    def right(self, **kwargs):
        return super().right(**kwargs)

    @_retry
    def left(self, **kwargs):
        return super().left(**kwargs)

    @_retry
    def up(self, **kwargs):
        return super().up(**kwargs)

    @_retry
    def down(self, **kwargs):
        return super().down(**kwargs)

    def __getitem__(self, instance: int):
        return Element(ui_object=super().__getitem__(instance))

    def __get__(self, instance, owner):
        """
        :param instance:    持有该类的父类实例（appuiautomator.u2.page.Page）
        :param owner:       持有该类的父类实例（appuiautomator.u2.page.Page）
        :return:
        """
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__find(instance.device)  # 将Page对象的device属性传递给PageElement对象

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')


class XPathElement(XPathSelector):
    def __init__(self,
                 xpath,
                 xpath_selector: XPathSelector = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):
        if not xpath:
            raise ValueError('请指定元素xpath的定位信息')

        if xpath_selector:
            # 直接把XPathSelector的属性字典复制过来
            self.__dict__.update(xpath_selector.__dict__)

        self.xpath = xpath
        self.delay = delay
        self.timeout = timeout
        self.interval = interval

    def __find(self, device: Device):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = device.xpath(self.xpath)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
            else:
                raise XPathElementNotFoundError(self._xpath_list)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            element = device.xpath(self.xpath)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
        raise XPathElementNotFoundError(self._xpath_list)

    def child(self, xpath):
        return Element(super().child(xpath))

    def __get__(self, instance, owner):
        """
        :param instance:    持有该类的父类实例（appuiautomator.u2.page.Page）
        :param owner:       持有该类的父类实例（appuiautomator.u2.page.Page）
        :return:
        """
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__find(instance.device)  # 将Page对象的device属性传递给PageElement对象

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')
