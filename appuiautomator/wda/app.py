#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app.py
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
from appuiautomator.exceptions import AppException
from appuiautomator.utils.log_util import get_logger
from appuiautomator.wda import Page

from wda import Client

log = get_logger(__name__)


class App:
    bundle_id = None  # type: str
    url = None  # type: str

    def __new__(cls, client: Client):
        # App实例化时遍历App实例的属性，如果含有Page类，则把device赋值给page
        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将App的client赋值给Page
                attr.client = client
        return super(App, cls).__new__(cls)

    def __init__(self, client: Client):
        if not self.bundle_id:
            raise AppException('BundleID不允许为空')
        self.client = client
