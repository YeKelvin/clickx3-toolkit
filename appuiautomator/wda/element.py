#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/18 11:17
# @Author  : Kelvin.Ye
from time import sleep

from appuiautomator.exceptions import ElementException
from appuiautomator.utils.log_util import get_logger

from wda import Selector
from wda.exceptions import WDAElementNotFoundError

log = get_logger(__name__)


class Locator(dict):
    ...


class Element(Selector):
    def __init__(self,
                 selector: Selector = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5,
                 **kwargs):
        if selector:
            # 直接把Selector的属性字典复制过来
            self.__dict__ = selector.__dict__

        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.kwargs = kwargs

    def __find(self, client):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            selector = client(**self.kwargs)
            if selector.exists:
                self.__dict__.update(selector.__dict__)
                return self
            else:
                raise WDAElementNotFoundError(str(self.kwargs))

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            selector = client(**self.kwargs)
            if selector.exists:
                self.__dict__.update(selector.__dict__)
                return self
        raise WDAElementNotFoundError(str(self.kwargs))

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__find(instance.client)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')
