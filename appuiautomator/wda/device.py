#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device.py
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
from wda import Client


class Device(Client):
    """IOS设备类
    """

    def __init__(self, wda_client: Client):
        self.__dict__ = wda_client.__dict__
