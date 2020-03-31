#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2019/8/27 11:57
# @Author  : Kelvin.Ye
from enum import Enum, unique

from appuiautomator.element import Element, Location
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class AutomatedClient:
    pass


class MobileDevice:
    """设备基类
    """
    # 设备类型
    type = None

    def __init__(self,
                 address: str,
                 app,
                 shell,
                 session,
                 keyevent,
                 gesture,
                 screen) -> None:
        self.address = address
        self.app = app
        self.shell = shell
        self.session = session
        self.keyevent = keyevent
        self.gesture = gesture
        self.screen = screen

    def find_element(self, location, timeout) -> Element:
        pass

    def watcher(self, name):
        pass

    def get_device(self):
        pass

    def push(self, src, dst):
        """将文件推送到设备
        """
        pass

    def pull(self, src: str, dst: str):
        """从设备中提取文件，如果在设备上找不到该文件
        """
        pass

    def healthcheck(self):
        """检查并维持设备端守护进程处于运行状态
        """
        pass


@unique
class DeviceType(Enum):
    ANDROID = 'Android'
    IOS = 'IOS'
