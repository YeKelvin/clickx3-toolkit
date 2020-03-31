#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : android.py
# @Time    : 2019-09-16 21:12
# @Author  : KelvinYe
from datetime import datetime
from enum import unique, Enum
from typing import Union

import uiautomator2 as u2
from uiautomator2 import Device

from appuiautomator import MobileDevice
from appuiautomator.element import Element
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class AndroidDevice(MobileDevice):
    # 设备类型
    type = 'Android'

    def __init__(self, address: str, timeout: int = 5) -> None:
        self.d = u2.connect(address)
        self.d.implicitly_wait(timeout)
        super().__init__(address,
                         AndroidAppManager(self.d),
                         AndroidShell(self.d),
                         AndroidSession(self.d),
                         AndroidKeyEvents(self.d),
                         AndroidGesture(self.d),
                         AndroidScreen(self.d))

    def find_element(self, location: dict, timeout: int = None) -> Element:
        return Element(self.d, location, timeout)

    def watcher(self, name: str) -> Device('').watcher(''):
        return self.d.watcher(name)

    def get_device(self) -> Device:
        return self.d

    def push(self, src: any, dst: str):
        """将文件推送到设备

        :example:   d.push("foo.txt", "/sdcard/")           push
                    d.push("foo.txt", "/sdcard/bar.txt")    push and rename
        :param src: 文件源
        :param dst: 目录路径
        :return:
        """
        self.d.push(src, dst)

    def pull(self, src: str, dst: str):
        """从设备中提取文件，如果在设备上找不到该文件

        :example:       d.pull("/sdcard/tmp.txt", "tmp.txt")
        :param src:     文件源
        :param dst:     目录路径
        :return:
        :raise:         FileNotFoundError
        """
        self.d.pull(src, dst)

    def healthcheck(self):
        """检查并维持设备端守护进程处于运行状态
        """
        return self.d.healthcheck()


class AndroidAppManager:
    """app管理类
    """

    def __init__(self, d: Device) -> None:
        self.d = d

    def install(self, url: str):
        """安装app
        """
        self.d.app_install(url)

    def start(self, package_name: str):
        """启动app
        """
        self.d.app_start(package_name)

    def stop(self, package_name: str):
        """停止app
        """
        self.d.app_stop(package_name)

    def clear_cache(self, package_name: str):
        """清除app数据
        """
        self.d.app_clear(package_name)

    def stop_all(self, excludes=None):
        """停止所有app
        """
        if excludes is None:
            excludes = []
        self.d.app_stop_all(excludes)

    def wait(self, package_name: str, timeout: float = 20.0, front=False):
        """等待 app运行

        :param package_name:    app包名称
        :param timeout:         最长等待时间
        :param front:           是否等待应用前台运行
        :return:
        """
        pid = self.d.app_wait(package_name, timeout, front)
        if not pid:
            log.info(f'{package_name} is not running')
        else:
            log.debug(f'{package_name} pid is {pid}')


class AndroidShell:
    """执行 adb shell命令
    """

    def __init__(self, d: Device) -> None:
        self.d = d

    def input(self, input_content: str) -> None:
        """通过adb shell input text 进行内容输入
        不限于字母、数字、汉字等
        """
        log.info(f'input text {input_content}')
        self.d.shell(f'input text {input_content}')

    def refresh_gallery(self, file_uri: str) -> None:
        """上传图片至系统图库后，要手动广播通知系统图库刷新
        """
        log.info('android.intent.action.MEDIA_SCANNER_SCAN_FILE 广播刷新系统图库')
        if file_uri.startswith('/'):
            file_uri = file_uri[1:]
        self.d.shell(fr'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{file_uri}')

    def screencap(self, path: str = None) -> None:
        """设备本地截图
        """
        if path:
            command = f'screencap -p {path}'
        else:
            current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
            filename = f'Screenshot_{current_time}.png'
            command = f'screencap -p /sdcard/DCIM/Screenshots/{filename}'
        self.d.shell(command)


class AndroidSession:
    """会话代表应用程序生命周期。可用于启动应用，检测应用崩溃
    """

    def __init__(self, d: Device) -> None:
        self.d = d

    def implicitly_wait(self, seconds=None):
        """设置隐式等待时间
        """
        self.d.implicitly_wait(seconds)


class AndroidKeyEvents:
    """按钮事件
    """

    def __init__(self, d: Device) -> None:
        self.d = d


class AndroidGesture:
    """手势事件
    """

    def __init__(self, d: Device) -> None:
        self.d = d

    def click(self, x, y):
        """单击屏幕
        """
        self.d.click(x, y)

    def double_click(self, x, y, duration=0.1):
        """双击屏幕
        """
        self.d.double_click(x, y, duration)

    def long_click(self, x, y, duration=0.5):
        """长按屏幕
        """
        self.d.long_click(x, y, duration)

    def swipe(self, sx, sy, ex, ey, duration=0.5):
        """滑动屏幕
        """
        self.d.swipe(sx, sy, ex, ey, duration)

    def swipe_ext(self, direction: str, scale: float = 0.9, box: Union[None, tuple] = None):
        """滑动屏幕

        :param direction:   left（屏幕左滑）| right（屏幕右滑）| up（屏幕上滑）| bottom（屏幕下滑）
        :param scale:       滑动距离（屏幕宽度的百分比）
        :param box:         在固定区域做滑动
        :return:
        """
        self.d.swipe_ext(direction, scale, box)

    def drag(self, sx, sy, ex, ey, duration=0.5):
        """拖动
        """
        self.d.drag(sx, sy, ex, ey, duration)

    def swipe_points(self, points: list, duration=0.2):
        self.d.swipe_points(points, duration)


class AndroidScreen:
    """屏幕类
    """

    def __init__(self, d: Device) -> None:
        self.d = d


@unique
class KeyCode(Enum):
    home = 'home'
    back = 'back'
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'
    center = 'center'
    menu = 'menu'
    search = 'search'
    enter = 'enter'
    delete = 'delete'
    recent = 'recent'  # Show all apps
    volume_up = 'volume_up'
    volume_down = 'volume_down'
    volume_mute = 'volume_mute'
    camera = 'camera'
    power = 'power'
    alt_left = '0x00000039'  # 57
    alt_right = '0x0000003a'  # 58
    caps_lock = '0x00000073'  # 115 Caps Lock key
    clear = '0x0000001c'  # 28 Clear key
    copy = '0x00000116'  # 278
    cut = '0x00000115'  # 277
    ctrl_left = '0x00000071'  # 113
    ctrl_right = '0x00000072'  # 114
    left_bracket = '0x00000047'  # 71 [
    page_up = '0x0000005c'  # 92
    page_down = '0x0000005d'  # 93
    plus = '0x00000051'  # 81 +
    pound = '0x00000012'  # 18 #
    at = '0x0000004d'  # 77 @
    comma = '0x00000037'  # 55 ,
    equals = '0x00000046'  # 70 =
    space = '0x0000003e'  # 62
    semicolon = '0x0000004a'  # 74 ;
    shift_left = '0x0000003b'  # 59
    shift_right = '0x0000003c'  # 60
    slash = '0x0000004c'  # 76 /
    STAR = '0x00000011'  # 17 *
    tab = '0x0000003d'  # 61

    key_0 = '0x00000007'  # 7
    key_1 = '0x00000008'  # 8
    key_2 = '0x00000009'  # 9
    key_3 = '0x0000000a'  # 10
    key_4 = '0x0000000b'  # 11
    key_5 = '0x0000000c'  # 11
    key_6 = '0x0000000d'  # 11
    key_7 = '0x0000000e'  # 11
    key_8 = '0x0000000f'  # 11
    key_9 = '0x00000010'  # 11

    key_a = '0x0000001d'  # 29
    key_b = '0x0000001e'  # 30
    key_c = '0x0000001f'  # 31
    key_d = '0x00000020'  # 32
    key_e = '0x00000021'  # 33
    key_f = '0x00000022'  # 34
    key_g = '0x00000023'  # 35
    key_h = '0x00000024'  # 36
    key_i = '0x00000025'  # 37
    key_j = '0x00000026'  # 38
    key_k = '0x00000027'  # 39
    key_l = '0x00000028'  # 40
    key_m = '0x00000029'  # 41
    key_n = '0x0000002a'  # 42
    key_o = '0x0000002b'  # 43
    key_p = '0x0000002c'  # 44
    key_q = '0x0000002d'  # 45
    key_r = '0x0000002e'  # 46
    key_s = '0x0000002f'  # 47
    key_t = '0x00000030'  # 48
    key_u = '0x00000031'  # 49
    key_v = '0x00000032'  # 50
    key_w = '0x00000033'  # 51
    key_x = '0x00000034'  # 52
    key_y = '0x00000035'  # 53
    key_z = '0x00000036'  # 54

    key_f1 = '0x00000083'  # 131
    key_f2 = '0x00000084'  # 132
    key_f3 = '0x00000085'  # 133
    key_f4 = '0x00000086'  # 134
    key_f5 = '0x00000087'  # 135
    key_f6 = '0x00000088'  # 136
    key_f7 = '0x00000089'  # 137
    key_f8 = '0x0000008a'  # 138
    key_f9 = '0x0000008b'  # 139
    key_f10 = '0x0000008c'  # 140
    key_f11 = '0x0000008d'  # 141
    key_f12 = '0x0000008e'  # 142
