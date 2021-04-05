#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page.py
# @Time    : 2020/4/1 23:53
# @Author  : Kelvin.Ye
from appuiautomator.u2.app import App, Webview
from appuiautomator.u2.device import Device
from appuiautomator.utils.log_util import get_logger
from appuiautomator.exceptions import PageException

log = get_logger(__name__)


class Page:
    package_name = None  # type: str
    activity_name = None  # type: str
    url = None  # type: str

    def __init__(self):
        self.device: Device = None
        self.webview: Webview = None

    def __get__(self, instance, owner):
        if instance is None:
            raise PageException('持有类没有实例化')

        assert owner == App

        self.package_name = instance.package_name
        self.device = instance.device
        self.webview = instance.webview

        return self

    def __set__(self, instance, value):
        raise NotImplementedError('用不着')

    def to_here(self):
        if self.package_name and self.activity_name:
            self._open_page_by_activity()
            return

        if self.url:
            self._open_page_by_url()
            return

        raise PageException(f'没有提供package、activity或url，page:[ {self} ]')

    def to_here_by_activity(self):
        if self.package_name and self.activity_name:
            self._open_page_by_activity()

        raise PageException(f'没有提供package、activity，page:[ {self} ]')

    def to_here_by_url(self):
        if self.url:
            self._open_page_by_url()

        raise PageException(f'没有提供url，page:[ {self} ]')

    def _open_page_by_activity(self):
        log.info(f'通知指定Activity打开页面，activity:[ {self.activity} ]')
        self.device.app_start(self.package_name, self.activity)

    def _open_page_by_url(self):
        log.info(f'通知指定URL打开页面，url:[ {self.url} ]')
        self.device.open_url(self.url)
