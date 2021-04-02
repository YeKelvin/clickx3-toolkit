#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : decorators.py
# @Time    : 2021/04/02 16:22
# @Author  : Kelvin.Ye
from functools import wraps
from time import sleep

from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


def retry_assert(delay: float = 0, timeout: float = 5, interval: float = 1):
    def decorate(func):
        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 重试次数小于1时，不重试，断言失败直接抛异常
            if retry_count < 1:
                return func(*args, **kwargs)

            # 重试断言，断言成功时返回，断言失败时重试直到timeout后抛出异常
            for i in range(retry_count):
                try:
                    if i > 0:
                        sleep(interval)
                    return func(*args, **kwargs)
                except AssertionError:
                    if i == (retry_count - 1):
                        raise
                    log.info('重试断言')
                    continue
        return wrapper
    return decorate
