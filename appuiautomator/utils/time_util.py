#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : time_util.py
# @Time    : 2019/8/27 13:53
# @Author  : Kelvin.Ye
import time
from _datetime import datetime


def current_strftime() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def current_timestamp_as_ms() -> int:
    """获取毫秒级时间戳，用于计算毫秒级耗时
    """
    return int(time.time() * 1000)


def current_timestamp_as_s() -> int:
    """获取秒级时间戳，用于计算秒级耗时
    """
    return int(time.time())


current_timestamp_precision = {
    'ms': current_timestamp_as_ms,
    's': current_timestamp_as_s
}


def current_timestamp(precision='ms') -> int:
    return current_timestamp_precision.get(precision)()


def seconds_to_hms(seconds: int) -> str:
    """秒数转换为时分秒
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%02dh:%02dm:%02ds' % (h, m, s)
