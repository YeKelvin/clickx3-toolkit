#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app.py
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
from clickx3.common.exceptions import AppException
from clickx3.utils.log_util import get_logger
from clickx3.wda.device import Device


log = get_logger(__name__)


class IOSApp:
    bundle_id = None  # type: str
    url = None  # type: str

    def __init__(self, device: Device, env: str = None):
        if not self.bundle_id:
            raise AppException('BundleID不允许为空')

        self.device = device
        self.env = env
