#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device.py
# @Time    : 2020/4/3 10:46
# @Author  : Kelvin.Ye
from datetime import datetime
from time import sleep

import uiautomator2 as u2

from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


def connect(addr=None):
    return Device(u2.connect(addr))


class Device(u2.Device):
    """安卓设备类
    """

    def __init__(self, u2d):
        self.__dict__ = u2d.__dict__

    def activity_start_by_uri(self, uri):
        self.shell(f'am start -a android.intent.action.VIEW -d {uri}')

    def app_restart(self, package_name, activity=None):
        log.info(f'restarting app {package_name}')
        self.stop(package_name)
        self.start(package_name, activity)
        self.wait(package_name)

    def save_app_icon(self, package_name, path):
        """保存 app图标
        """
        icon = self.app_icon(package_name)
        icon.save(path)

    def fastinput_ime(self, text):
        self.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        sleep(0.5)
        self.send_keys(text)  # adb广播输入
        sleep(0.5)
        self.set_fastinput_ime(False)  # 切换成正常的输入法

    def save_screenshot(self, destination):
        """保存截图
        """
        image = self.screenshot()
        image.save(destination)

    def adb_input(self, input_content: str) -> None:
        """通过adb shell input text 进行内容输入，不限于字母、数字、汉字等
        """
        log.info(f'adb input text {input_content}')
        self.shell(f'input text {input_content}')

    def adb_refresh_gallery(self, file_uri: str) -> None:
        """上传图片至系统图库后，要手动广播通知系统图库刷新
        """
        log.info('android.intent.action.MEDIA_SCANNER_SCAN_FILE 广播刷新系统图库')
        if file_uri.startswith('/'):
            file_uri = file_uri[1:]
        self.shell(fr'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{file_uri}')

    def adb_screencap(self, path: str = None) -> None:
        """设备本地截图
        """
        if path:
            command = f'screencap -p {path}'
        else:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'Screenshot_{current_time}.png'
            command = f'screencap -p /sdcard/DCIM/Screenshots/{filename}'
        self.shell(command)

    def get_toast_message(self):
        toast_msg = self.toast.get_message(3.0)
        log.info(f'toast message={toast_msg}')
        return toast_msg
