#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/17 21:29
# @Author  : Kelvin.Ye
from functools import wraps
from time import sleep

from uiautomator2 import UiObject
from uiautomator2.exceptions import UiObjectNotFoundError
from uiautomator2.exceptions import XPathElementNotFoundError
from uiautomator2.xpath import XMLElement
from uiautomator2.xpath import XPathSelector

from clickx3.common.exceptions import ElementException
from clickx3.common.exceptions import TimeoutException
from clickx3.u2.device import Device
from clickx3.u2.support import expected_conditions as EC
from clickx3.u2.support.wait import U2DeviceWait
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class Locator(dict):
    ...


def retry_find_u2element(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)
        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = func(*args, **kwargs)
            if element.exists:
                return Element(ui_object=element)
            else:
                raise UiObjectNotFoundError(
                    {
                        'code': -32002,
                        'message': 'retry find element timeout',
                        'data': str(element.selector)
                    },
                    method='@retry_find_u2element')

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(interval)
            element = func(*args, **kwargs)
            if element.exists:
                return Element(ui_object=element)
        raise UiObjectNotFoundError(
            {
                'code': -32002,
                'message': 'retry find element timeout',
                'data': str(element.selector)
            },
            method='@retry_find_u2element')
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

        self._delay = delay
        self._timeout = timeout
        self._interval = interval
        self._kwargs = kwargs
        self.wait = ElementWait(self)

    def __retry_find(self, device: Device):
        # 计算重试次数
        retry_count = int(float(self._timeout) / float(self._interval))
        # 延迟查找元素
        if self._delay:
            sleep(self._delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = device(**self._kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
            else:
                raise UiObjectNotFoundError(
                    {
                        'code': -32002,
                        'message': 'retry find element timeout',
                        'data': str(element.selector)
                    },
                    method='Element.__retry_find')  # yapf: disable

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self._interval)
            element = device(**self._kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
        raise UiObjectNotFoundError(
            {
                'code': -32002,
                'message': 'retry find element timeout',
                'data': str(element.selector)
            },
            method='Element.__retry_find')  # yapf: disable

    def __scroll_find(self, method, **kwargs):
        allow_scroll_find = kwargs.pop('allow_scroll_find', True)

        if allow_scroll_find and self.info['scrollable']:
            log.info(f'滚动至目标元素，locator:[ {kwargs} ]')
            if self.scroll.to(**kwargs):
                return method(**kwargs)
            else:
                raise UiObjectNotFoundError(
                    {
                        'code': -32002,
                        'message': 'scrool to target element failed',
                        'data': str(kwargs)
                    },
                    method='Element.__scroll_to_find')
        else:
            return method(**kwargs)

    @retry_find_u2element
    def child(self, **kwargs):
        """查找子元素

        Args:
            delay (float, 0.5): 延迟查找等待时间
            timeout (float, 10): 重试查找超时时间
            interval (float, 0.5): 重试查找间隔时间
            allow_scroll_find (bool, True): 是否允许滚动至目标元素

        Returns:
            Element
        """
        return self.__scroll_find(super().child, **kwargs)

    @retry_find_u2element
    def sibling(self, **kwargs):
        return self.__scroll_find(super().sibling, **kwargs)

    @retry_find_u2element
    def right(self, **kwargs):
        return self.__scroll_find(super().right, **kwargs)

    @retry_find_u2element
    def left(self, **kwargs):
        return self.__scroll_find(super().left, **kwargs)

    @retry_find_u2element
    def up(self, **kwargs):
        return self.__scroll_find(super().up, **kwargs)

    @retry_find_u2element
    def down(self, **kwargs):
        return self.__scroll_find(super().down, **kwargs)

    def __getitem__(self, instance: int):
        return Element(ui_object=super().__getitem__(instance))

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__retry_find(instance.device)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')


class XPathElement(XMLElement):

    def __init__(self,
                 xpath,
                 xpath_selector: XPathSelector = None,
                 xml_element: XMLElement = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):

        if not xpath:
            raise ValueError('xpath不允许为空')

        if xpath_selector:
            self._xpath_selector = xpath_selector

        if xml_element:
            # 直接把XMLElement的属性字典复制过来
            self.__dict__.update(xml_element.__dict__)

        self._xpath = xpath
        self._delay = delay
        self._timeout = timeout
        self._interval = interval

    def __retry_find(self, device: Device):
        # 计算重试次数
        retry_count = int(float(self._timeout) / float(self._interval))
        # 延迟查找元素
        if self._delay:
            sleep(self._delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            xpath_selector = device.xpath(self._xpath)
            if xpath_selector.exists:
                xml_element = xpath_selector.get()
                self._xpath_selector = xpath_selector
                self.__dict__.update(xml_element.__dict__)
                return self
            else:
                raise XPathElementNotFoundError(self._xpath_list)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self._interval)
            xpath_selector = device.xpath(self._xpath)
            if xpath_selector.exists:
                xml_element = xpath_selector.get()
                self._xpath_selector = xpath_selector
                self.__dict__.update(xml_element.__dict__)
                return self
        raise XPathElementNotFoundError(self._xpath_list)

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__retry_find(instance.device)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')

    def child(self, xpath):
        raise NotImplementedError('用到再写吧')


class XPathElements(list):

    @property
    def count(self):
        return len(self)

    def __init__(self,
                 xpath,
                 xpath_selector: XPathSelector = None,
                 xml_elements: list = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):

        if not xpath:
            raise ValueError('xpath不允许为空')

        if xpath_selector:
            self._xpath_selector = xpath_selector

        if xml_elements:
            self.extend(xml_elements)

        self._xpath = xpath
        self._delay = delay
        self._timeout = timeout
        self._interval = interval

    def __retry_find(self, device: Device):
        # 计算重试次数
        retry_count = int(float(self._timeout) / float(self._interval))
        # 延迟查找元素
        if self._delay:
            sleep(self._delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            xpath_selector = device.xpath(self._xpath)
            if xpath_selector.exists:
                xml_elements = xpath_selector.all()
                self._xpath_selector = xpath_selector
                self.extend(xml_elements)
                return self
            else:
                raise XPathElementNotFoundError(self._xpath_list)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self._interval)
            xpath_selector = device.xpath(self._xpath)
            if xpath_selector.exists:
                xml_elements = xpath_selector.all()
                self._xpath_selector = xpath_selector
                self.extend(xml_elements)
                return self
        raise XPathElementNotFoundError(self._xpath_list)

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__retry_find(instance.device)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')

    def __getitem__(self, index: int):
        item = super().__getitem__(index)
        if isinstance(item, XPathElement):
            return item
        elif isinstance(item, XMLElement):
            return XPathElement(xpath_selector=self._xpath_selector, xml_element=item)
        else:
            raise ElementException(f'仅支持clickx3.XPathElement和uiautomator2.XMLElement，object:[ {item} ]')


class ElementWait:

    def __init__(self, element=None):
        self.element = element

    def _selector_to_str(self, errmsg):
        errmsg = f'errmsg:[ {errmsg} ] ' if errmsg else ''
        return errmsg + f'selector:[ {self.element._kwargs} ]'

    def _wait_until(self, method, timeout, errmsg):
        errmsg = self._selector_to_str(errmsg)
        timeout = timeout or self.element._timeout
        return U2DeviceWait(None, timeout).until(method, message=errmsg)

    def text_contains(self, expected, timeout=None, errmsg=None):
        log.info(f'等待元素text包含:[ {expected} ]')
        try:
            return self._wait_until(EC.text_contains_of(self.element, expected), timeout, errmsg)
        except TimeoutException:
            log.error(f'等待超时，当前元素text:[ {self.element.text} ]')
            raise
