#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
import wda


class Device(wda.Client):
    """IOS设备类
    """

    def __init__(self, wdac):
        self.__dict__ = wdac.__dict__
