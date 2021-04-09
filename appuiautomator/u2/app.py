#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app.py
# @Time    : 2020/4/3 10:47
# @Author  : Kelvin.Ye
from selenium import webdriver
from appuiautomator.u2.device import Device
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class AndroidApp:
    package_name = None  # type: str
    activity_name = None  # type: str
    url = None  # type: str

    def __init__(self, device: Device):
        self.device = device
        self.webview = Webview(self)

    def start(self):
        log.info(f'启动app，package:[ {self.package_name} ]，activity:[ {self.activity_name} ]')
        self.device.app_start(self.package_name, activity=self.activity_name)
        self.wait()

    def start_by_url(self):
        log.info(f'通过指定url启动app，url:[ {self.url} ]')
        self.device.open_url(self.url)
        self.wait()

    def stop(self):
        log.info(f'停止app，package:[ {self.package_name} ]')
        self.device.app_stop(self.package_name)

    def wait(self):
        log.info(f'等待app启动且在前台，package:[ {self.package_name} ]')
        self.device.app_wait(self.package_name, front=True)

    def clear(self):
        log.info(f'清空app缓存，package:[ {self.package_name} ]')
        self.device.app_clear(self.package_name)

    def clear_and_start(self):
        self.clear()
        self.start()

    def restart(self):
        log.info(f'重启app，package:[ {self.package_name} ]')
        self.stop()
        self.start()


class Webview:
    def __init__(self, app):
        self.driver = None  # type: webdriver
        self.app = app

    def initialize(self):
        current_app = self.app.device.app_current()
        if self.app.package_name != current_app['package']:
            self.app.start()

        from appuiautomator.se.chromedriver import webview_driver
        self.driver = webview_driver(
            serial=self.app.device.serial,
            package=self.app.package_name,
            process=self.app.package_name,
            activity=self.app.activity_name or self.app.device.app_current()['activity'])
        self.app.webview = self
