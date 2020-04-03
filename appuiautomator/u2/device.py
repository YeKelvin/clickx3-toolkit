#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device.py
# @Time    : 2020/4/3 10:46
# @Author  : Kelvin.Ye
from datetime import datetime
from typing import Union

import uiautomator2 as u2

from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Device:
    def __init__(self, driver):
        self.d: u2.Device = driver

    def run_adb_shell(self, command, timeout=60):
        output, exit_code = self.d.shell(command, timeout=timeout)
        return output, exit_code

    @property
    def info(self):
        """基础信息
        """
        return self.d.info

    @property
    def device_info(self):
        """设备详细信息
        """
        return self.d.device_info

    @property
    def serial(self):
        """当前设备号
        """
        return self.d.serial

    @property
    def wlan_ip(self):
        """wlan地址
        """
        return self.d.wlan_ip

    @property
    def clipboard(self):
        """剪贴板内容
        """
        return self.d.clipboard

    @property
    def orientation(self):
        """屏幕方向，可能的值：natural | left | right | upsidedown
        """
        return self.d.orientation

    def set_orientation(self, direction):
        """设置屏幕方向

        Args:
            direction:屏幕方向，枚举：natural | left | right | upsidedown

        Returns:

        """
        self.d.set_orientation(direction)

    def freeze_rotation(self):
        """冻结旋转
        """
        self.d.freeze_rotation()

    def unfreeze_rotation(self):
        """解除冻结旋转
        """
        self.d.freeze_rotation(False)

    def set_clipboard(self, text, label=None):
        """设置剪贴板内容
        """
        self.d.set_clipboard(text, label)

    def window_size(self):
        """窗口大小
        """
        return self.d.window_size()

    def app_current(self):
        """当前前台 app信息
        """
        return self.d.app_current()

    def wait_activity(self, activity_name):
        """等待 activity出现
        """
        return self.d.wait_activity(activity_name)

    def app_install(self, url):
        """安装 app
        """
        self.d.app_install(url)

    def app_start(self, package_name):
        """运行 app
        """
        print(f'starting {package_name}')
        self.d.app_start(package_name)

    def app_stop(self, package_name):
        """停止 app
        """
        self.d.app_stop(package_name)

    def app_clear(self, package_name):
        """清空 app缓存
        """
        self.d.app_clear(package_name)

    def app_stop_all(self, excludes=[]):
        """停止所有 app
        """
        self.d.app_stop_all(excludes)

    def app_info(self, package_name):
        """app的详细信息"""

        return self.d.app_info(package_name)

    def save_app_icon(self, package_name, path):
        """保存 app图标
        """
        icon = self.d.app_icon(package_name)
        icon.save(path)

    def app_list_running(self):
        """获取正在运行的 app
        """
        return self.d.app_list_running()

    def app_wait(self, package_name, front=True, timeout=5):
        """等待应用运行
        """
        pid = self.d.app_wait(package_name, front=front, timeout=timeout)
        return pid

    def push(self, source, destination):
        """推送文件到设备
        """
        self.d.push(source, destination)

    def pull(self, source, destination):
        """从设备拉文件到本地
        """
        self.d.pull(source, destination)

    def screen_on(self):
        """打开屏幕
        """
        self.d.screen_on()

    def screen_off(self):
        """关闭屏幕
        """
        self.d.screen_off()

    def unlock(self):
        """锁屏
        """
        self.d.unlock()

    def press(self, key):
        """按键
        """
        self.d.press(key)

    def fastinput_ime(self, text):
        self.d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        self.d.send_keys(text)  # adb广播输入
        self.d.set_fastinput_ime(False)  # 切换成正常的输入法

    def clear_text(self):
        """除输入框所有内容
        """
        self.d.clear_text()

    def click(self, x, y):
        """单击屏幕
        """
        self.d.click(x, y)

    def double_click(self, x, y, duration=0.1):
        """双击屏幕
        """
        self.d.double_click(x, y, duration)

    def long_click(self, x, y, duration=0.1):
        """长按屏幕
        """
        self.d.double_click(x, y, duration)

    def swipe(self, sx, sy, ex, ey, duration=1):
        """滑动屏幕
        """
        self.d.swipe(sx, sy, ex, ey, duration)

    def swipe_ext(self, direction: str, scale: float = 0.9, box: Union[None, tuple] = None):
        """屏幕滑动

        Args:
            direction:  滑动方向，枚举：left | right | up | down
            scale:      滑动距离为屏幕宽度的百分比
            box:        在指定区域内滑动，如：(0,0) -> (100, 100)

        Returns:

        """
        self.d.swipe_ext(direction, scale, box)

    def drag(self, sx, sy, ex, ey, duration=0.5):
        """拖动
        """
        self.d.drag(sx, sy, ex, ey, duration)

    def save_screenshot(self, destination):
        """保存截图
        """
        image = self.d.screenshot()
        image.save(destination)

    def defdump_hierarchy(self):
        """获取UI层次结构
        """
        xml = self.d.dump_hierarchy()
        return xml

    def open_notification(self):
        """打开通知栏
        """
        self.d.open_notification()

    def open_quick_settings(self):
        """打开设置
        """
        self.d.open_quick_settings()

    def watcher(self):
        return self.d.watcher

    def remove_watcher(self, name):
        """移除指定名称的监控
        """
        self.d.watcher.remove(name)

    def remove_all_watcher(self):
        """移除所有的监控
        """
        self.d.watcher.remove()

    def start_watcher(self, interval: float = 2.0):
        """开始后台监控
        """
        self.d.watcher.start(interval)

    def run_watcher(self):
        """强制运行所有监控
        """
        self.d.watcher.run()

    def stop_watcher(self):
        """停止监控
        """
        self.d.watcher.stop()

    def reset_watcher(self):
        """停止并移除所有的监控，常用于初始化
        """
        self.d.watcher.reset()

    def show_toast(self, text, duration=1.0):
        """弹出 Toast
        """
        self.d.toast.show(text, duration)

    def get_toast(self, wait_timeout=10, cache_timeout=10, default=None):
        """获取 Toast内容
        """
        self.d.toast.get_message(wait_timeout, cache_timeout, default)

    def reset_toast(self):
        """清除 Toast缓存
        """
        self.d.toast.reset()

    def adb_input(self, input_content: str) -> None:
        """通过adb shell input text 进行内容输入，不限于字母、数字、汉字等
        """
        log.info(f'input text {input_content}')
        self.run_adb_shell(f'input text {input_content}')

    def adb_refresh_gallery(self, file_uri: str) -> None:
        """上传图片至系统图库后，要手动广播通知系统图库刷新
        """
        log.info('android.intent.action.MEDIA_SCANNER_SCAN_FILE 广播刷新系统图库')
        if file_uri.startswith('/'):
            file_uri = file_uri[1:]
        self.run_adb_shell(fr'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{file_uri}')

    def adb_screencap(self, path: str = None) -> None:
        """设备本地截图
        """
        if path:
            command = f'screencap -p {path}'
        else:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'Screenshot_{current_time}.png'
            command = f'screencap -p /sdcard/DCIM/Screenshots/{filename}'
        self.run_adb_shell(command)
