#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ios.py
# @Time    : 2019-09-16 21:12
# @Author  : KelvinYe
from appuiautomator import MobileDevice
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class IOSDevice(MobileDevice):
    # 设备类型
    type = 'IOS'
    pass
