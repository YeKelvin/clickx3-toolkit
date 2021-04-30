#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device.py
# @Time    : 2020/4/3 10:46
# @Author  : Kelvin.Ye
from datetime import datetime
import time

import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError
from uiautomator2.exceptions import XPathElementNotFoundError

from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class Device(u2.Device):
    """Android设备类，封装Uiautomator2的Device类
    """

    @staticmethod
    def connect(source):
        """连接Android设备

        Args:
            source (str): address or serial number

        Returns:
            Device
        """
        log.info(f'连接Android设备成功，设备号or地址:[ {source} ]')
        d = u2.connect(source)
        log.info(f'设备信息:[ {d.info} ]')
        return Device(d)

    def __init__(self, u2d: u2.Device):
        # 直接把u2.Device的属性字典复制过来
        self.__dict__ = u2d.__dict__

    def sleep(self, secs: float = 1):
        log.info(f'等待 {secs}s')
        time.sleep(secs)

    def adb_shell(self, command: str):
        log.info(f'执行adb命令:[ {command} ]')
        output, exit_code = self.shell(command)
        log.info(f'adb shell output:\n {output}')
        log.info(f'adb shell exitCode:[ {exit_code} ]')

    def open_url(self, url: str):
        self.adb_shell(f'am start -a android.intent.action.VIEW -d "{url}"')

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
        self.sleep(0.5)
        log.info(f'输入:[ {text} ]')
        self.send_keys(text)  # adb广播输入
        self.sleep(0.5)
        self.set_fastinput_ime(False)  # 切换成正常的输入法
        log.info('切换为正常的输入法')

    def adb_input(self, input_content: str) -> None:
        """通过adb shell input text 进行内容输入，不限于字母、数字、汉字等
        """
        self.adb_shell(f'input text {input_content}')

    def adb_refresh_gallery(self, file_uri: str) -> None:
        """上传图片至系统图库后，要手动广播通知系统图库刷新
        """
        log.info('ADB广播刷新系统图库')
        if file_uri.startswith('/'):
            file_uri = file_uri[1:]
        self.adb_shell(fr'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{file_uri}')

    def adb_screencap_local(self, path: str = None) -> None:
        """设备本地截图
        """
        if not path:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'screenshot_{current_time}.png'
            path = f'/sdcard/DCIM/Screenshots/{filename}'

        command = f'screencap -p {path}'
        self.adb_shell(command)

    def get_toast_message(self, wait_timeout=10, cache_timeout=10, default=None):
        log.info('获取toast信息')
        toast_msg = self.toast.get_message(wait_timeout, cache_timeout, default)
        log.info(f'toast:[ {toast_msg} ]')
        return toast_msg

    # TODO: 考虑优化，e.g.: exists().then().catch().error()
    def click_exists(self, **kwargs):
        try:
            log.info('如果元素存在且可见时点击元素')
            xpath = kwargs.pop('xpath', None)
            if xpath:
                element = self._retry_find_xpath_element(xpath)
            else:
                element = self._retry_find_element(**kwargs)
            element.click()
        except UiObjectNotFoundError:
            log.info(f'元素不存在或不可见，无需点击，selector:[ {kwargs} ]')
        except XPathElementNotFoundError:
            log.info(f'元素不存在或不可见，无需点击，xpath:[ {xpath} ]')

    def _retry_find_element(self, **kwargs):
        from clickx3.u2.element import Element

        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 2)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            time.sleep(delay)
        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = self(**kwargs)
            if element.exists:
                return Element(ui_object=element)
            else:
                raise UiObjectNotFoundError(
                    {
                        'code': -32002,
                        'message': 'retry find element timeout',
                        'data': str(element.selector)
                    },
                    method='Device._retry_find_element')

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                time.sleep(interval)
            element = self(**kwargs)
            if element.exists:
                return Element(ui_object=element)
        raise UiObjectNotFoundError(
            {
                'code': -32002,
                'message': 'retry find element timeout',
                'data': str(element.selector)
            },
            method='Device._retry_find_element')

    def _retry_find_xpath_element(self, xpath, **kwargs):
        from clickx3.u2.element import XPathElement

        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 2)
        interval = kwargs.pop('interval', 0.5)
        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            time.sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            xpath_selector = self.xpath(xpath)
            if xpath_selector.exists:
                xml_element = xpath_selector.get()
                xml_element = xpath_selector.get()
                return XPathElement(xpath_selector=xpath_selector, xml_element=xml_element)
            else:
                raise XPathElementNotFoundError(xpath)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                time.sleep(interval)
            xpath_selector = self.xpath(xpath)
            if xpath_selector.exists:
                xml_element = xpath_selector.get()
                return XPathElement(xpath_selector=xpath_selector, xml_element=xml_element)
        raise XPathElementNotFoundError(xpath)
