#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device.py
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
import time

from appuiautomator.utils.log_util import get_logger

from wda import Client

log = get_logger(__name__)


class Device(Client):
    """IOS设备类
    """

    def __init__(self, wda_client: Client):
        self.__dict__ = wda_client.__dict__

    def sleep(self, secs: float = 1):
        log.info(f'等待 {secs}s')
        time.sleep(secs)
