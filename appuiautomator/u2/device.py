#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device.py
# @Time    : 2020/4/3 10:46
# @Author  : Kelvin.Ye
from datetime import datetime
from time import sleep

import uiautomator2 as u2

from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


def connect(addr=None):
    return Device(u2.connect(addr))


class Device(u2.Device):
    """安卓设备类，封装Uiautomator2的Device类
    """

    def __init__(self, u2d: u2.Device):
        # 直接把u2.Device的属性字典复制过来
        self.__dict__ = u2d.__dict__

    def wait(self, secs=0.5):
        sleep(secs)

    def run_adb_shell(self, command: str):
        log.info(f'执行adb命令:[ {command} ]')
        output, exit_code = self.shell(command)
        log.info(f'adb shell output:\n {output}')
        log.info(f'adb shell exitCode:[ {exit_code} ]')

    def open_url(self, url: str):
        self.run_adb_shell(f'am start -a android.intent.action.VIEW -d "{url}"')

    def app_restart(self, package_name, activity=None):
        log.info(f'重启app:[ {package_name} ]')
        self.stop(package_name)
        self.start(package_name, activity)
        self.wait(package_name)

    def save_app_icon(self, package_name, path):
        """保存 app图标
        """
        log.info(f'保存app图标:[ {package_name} ] 至:[ {path} ]')
        icon = self.app_icon(package_name)
        icon.save(path)

    def fastinput_ime(self, text: str):
        log.info('切换为FastInputIME输入法')
        self.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        sleep(0.5)
        log.info(f'输入:[ {text} ]')
        self.send_keys(text)  # adb广播输入
        sleep(0.5)
        self.set_fastinput_ime(False)  # 切换成正常的输入法
        log.info('切换为正常的输入法')

    def adb_input(self, input_content: str) -> None:
        """通过adb shell input text 进行内容输入，不限于字母、数字、汉字等
        """
        self.run_adb_shell(f'input text {input_content}')

    def adb_refresh_gallery(self, file_uri: str) -> None:
        """上传图片至系统图库后，要手动广播通知系统图库刷新
        """
        log.info('ADB广播刷新系统图库')
        if file_uri.startswith('/'):
            file_uri = file_uri[1:]
        self.run_adb_shell(
            fr'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{file_uri}')

    def adb_screencap_local(self, path: str = None) -> None:
        """设备本地截图
        """
        if not path:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'screenshot_{current_time}.png'
            path = f'/sdcard/DCIM/Screenshots/{filename}'

        command = f'screencap -p {path}'
        self.run_adb_shell(command)

    def get_toast_message(self, wait_timeout=10, cache_timeout=10, default=None):
        log.info('获取toast信息')
        toast_msg = self.toast.get_message(wait_timeout, cache_timeout, default)
        log.info(f'toast:[ {toast_msg} ]')
        return toast_msg
