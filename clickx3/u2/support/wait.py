#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : webdriver.py
# @Time    : 2021/4/15 12:53
# @Author  : Kelvin.Ye
import time

from uiautomator2.exceptions import UiObjectNotFoundError
from uiautomator2.exceptions import XPathElementNotFoundError

from clickx3.common.exceptions import TimeoutException
from clickx3.utils.log_util import get_logger


log = get_logger(__name__)

# 轮询频率（间隔等待时间）
POLL_FREQUENCY = 0.5
# 需要忽略的Exception列表
IGNORED_EXCEPTIONS = (UiObjectNotFoundError, XPathElementNotFoundError)


class U2DeviceWait(object):

    def __init__(self, device, timeout, poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        self._device = device
        self._timeout = timeout
        self._poll = poll_frequency
        # avoid the divide by zero
        if self._poll == 0:
            self._poll = POLL_FREQUENCY
        exceptions = list(IGNORED_EXCEPTIONS)
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:  # ignored_exceptions is not iterable
                exceptions.append(ignored_exceptions)
        self._ignored_exceptions = tuple(exceptions)

    def until(self, method, message=''):
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._device)
                if value:
                    return value
            except self._ignored_exceptions as e:
                stacktrace = getattr(e, 'stacktrace', None)
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        log.error(f'Stacktrace:\n{stacktrace}')
        raise TimeoutException(message)

    def until_not(self, method, message=''):
        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._device)
                if not value:
                    return value
            except self._ignored_exceptions:
                return True
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutException(message)
