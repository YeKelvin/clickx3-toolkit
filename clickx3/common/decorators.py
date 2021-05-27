#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : decorators.py
# @Time    : 2021/04/02 16:22
# @Author  : Kelvin.Ye
from functools import partial
from functools import wraps
from time import sleep

from clickx3.utils.log_util import get_logger


log = get_logger(__name__)


def retry_assert(func=None, count: int = 5, interval: float = 1):
    """重试断言

    Args:
        retry_count (int): 重试次数
        interval (float): 重试间隔时间
    """
    if func is None:
        return partial(retry_assert, count=count, interval=interval)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 重试次数小于1时，不重试，断言失败直接抛异常
        if count < 1:
            return func(*args, **kwargs)

        # 重试断言，断言成功时返回，断言失败时重试直到timeout后抛出异常
        for i in range(count):
            try:
                if i > 0:
                    sleep(interval)
                return func(*args, **kwargs)
            except AssertionError:
                if i == (count - 1):
                    raise
                log.info(f'断言失败，重试断言，剩余重试次数:[ {count - 1 - i} ]')
                continue

    return wrapper
