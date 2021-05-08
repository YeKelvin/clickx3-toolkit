#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/18 11:17
# @Author  : Kelvin.Ye
from time import sleep

from wda import Element as WDAElement
from wda import Selector
from wda.exceptions import WDAElementNotFoundError

from clickx3.common.exceptions import ElementException
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class Locator(dict):
    ...


class Element(WDAElement):
    def __init__(self,
                 selector: Selector = None,
                 element: WDAElement = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5,
                 **kwargs):

        if element:
            # 直接把Element的属性字典复制过来
            self.__dict__.update(element.__dict__)

        self.selector = selector
        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.kwargs = kwargs

    def __retry_find(self, device):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            selector = device(**self.kwargs)
            if selector.exists:
                element = selector.get()
                self.selector = selector
                self.__dict__.update(element.__dict__)
                return self
            else:
                raise WDAElementNotFoundError(self.kwargs)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            selector = device(**self.kwargs)
            if selector.exists:
                element = selector.get()
                self.selector = selector
                self.__dict__.update(element.__dict__)
                return self
        raise WDAElementNotFoundError(self.kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__retry_find(instance.device)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')

    def child(self, *args, **kwargs):
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('interval', 0.5)

        child_selector = self.selector.child(*args, **kwargs)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            if child_selector.exists:
                child_element = child_selector.get()
                return Element(selector=child_selector, element=child_element)
            else:
                raise WDAElementNotFoundError(self.kwargs)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(interval)
            if child_selector.exists:
                child_element = child_selector.get()
                return Element(selector=child_selector, element=child_element)
        raise WDAElementNotFoundError(self.kwargs)


class Elements(list):

    @property
    def count(self):
        return len(self)

    def __init__(self,
                 selector: Selector = None,
                 elements: list = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):
        if selector:
            self.selector = selector

        if elements:
            self.extend(elements)

        self.delay = delay
        self.timeout = timeout
        self.interval = interval

    def __retry_find(self, device):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            selector = device(**self.kwargs)
            if selector.exists:
                elements = selector.find_elements()
                self.selector = selector
                self.extend(elements)
                return self
            else:
                raise WDAElementNotFoundError(self.kwargs)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            selector = device(**self.kwargs)
            if selector.exists:
                elements = selector.find_elements()
                self.selector = selector
                self.extend(elements)
                return self
        raise WDAElementNotFoundError(self.kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__retry_find(instance.device)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')

    def __getitem__(self, index: int):
        item = super().__getitem__(index)
        if isinstance(item, Element):
            return item
        elif isinstance(item, WDAElement):
            return Element(selector=self.selector, element=item)
        else:
            raise TypeError(f'仅支持clickx3.Element和wda.WDAElement，object:[ {item} ]')
