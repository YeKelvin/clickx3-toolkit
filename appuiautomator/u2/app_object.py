#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app_object.py
# @Time    : 2020/4/3 10:47
# @Author  : Kelvin.Ye
import uiautomator2 as u2

from appuiautomator.exceptions import PageError, AppError
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class AppObject:
    package_name = None

    def __init__(self, device):
        if not self.package_name:
            raise AppError('App Package Name can not be empty.')
        self.device: Device = device
        self.driver: u2.Device = device.driver
        self.pages: list = []

    def start(self):
        self.device.app_start(self.package_name)

    def stop(self):
        self.device.app_stop(self.package_name)

    def wait(self):
        self.device.app_wait(self.package_name)

    def clear(self):
        self.device.app_clear(self.package_name)

    def restart(self):
        self.stop()
        self.start()
        self.wait()


class Page:
    def __init__(self, clazz):
        self.clazz = clazz

    def __get__(self, instance, owner):
        if instance is None:
            return None
        device = instance.device
        pages = instance.pages
        for page in pages:
            if isinstance(page, self.clazz):
                return page
        page = self.clazz(device)
        pages.append(page)
        return page

    def __set__(self, instance, value):
        raise PageError('Can not set value')
