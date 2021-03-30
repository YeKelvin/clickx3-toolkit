#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app.py
# @Time    : 2020/4/3 10:47
# @Author  : Kelvin.Ye
from typing import Optional

from appuiautomator.exceptions import AppException
from appuiautomator.u2.device import Device
from appuiautomator.u2.page import Page
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class App:
    package_name = None  # type: Optional[str]
    activity = None  # type: Optional[str]
    uri = None  # type: Optional[str]

    def __new__(cls, device: Device):
        # App实例化时遍历App实例的属性，如果含有Page类，则把device赋值给page
        for attr in cls.__dict__.values():
            if isinstance(attr, Page):  # 将App的device赋值给Page
                attr.device = device
        return super(App, cls).__new__(cls)

    def __init__(self, device: Device):
        if not self.package_name:
            raise AppException('PackageName不允许为空')
        self.device = device

    def start(self):
        log.info('启动APP')
        self.device.app_start(self.package_name, self.activity)

    def start_by_uri(self):
        log.info(f'打开APP LINK:[ {self.uri} ]')
        self.device.activity_start_by_uri(self.uri)

    def stop(self):
        log.info('停止APP')
        self.device.app_stop(self.package_name)

    def wait(self):
        log.info('等待APP启动')
        self.device.app_wait(self.package_name)

    def clear(self):
        log.info('清空APP缓存')
        self.device.app_clear(self.package_name)

    def clear_and_start(self):
        self.clear()
        self.start()
        self.wait()

    def restart(self):
        log.info('重启APP')
        self.stop()
        self.start()
        self.wait()
        self.device.wait()
