#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : device
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye
import wda


class Device:
    @property
    def current_bundle_id(self):
        """当前app的bundle_id"""
        return self.sesson.bundle_id

    @property
    def current_session_id(self):
        """当前session_id"""
        return self.sesson.id

    @property
    def orientation(self):
        """屏幕方向
        """
        return self.sesson.orientation

    @orientation.setter
    def orientation(self, direction):
        """设置屏幕方向
        """
        self.sesson.orientation = direction

    @property
    def scale(self):
        """Get UIKit scale factor
        """
        return self.sesson.scale

    def __init__(self, session):
        self.sesson: wda.Client = session

    def app_launch(self, bundle_id, arguments=[], environment={}, wait_for_quiescence=False):
        """启动app
        """
        self.sesson.app_launch(bundle_id, arguments, environment, wait_for_quiescence)

    def app_activate(self, bundle_id):
        """激活app
        """
        self.sesson.app_activate(bundle_id)

    def app_terminate(self, bundle_id):
        """终止app
        """
        self.sesson.app_terminate(bundle_id)

    def app_state(self, bundle_id):
        """app状态
        """
        return self.sesson.app_state(bundle_id)

    def implicitly_wait(self, timeout):
        """设置元素等待时间
        """
        self.sesson.implicitly_wait(timeout)

    def home(self):
        """按home键
        """
        self.sesson.home()

    def lock(self):
        """锁屏
        """
        self.sesson.lock()

    def unlock(self):
        """解锁
        """
        self.sesson.unlock()

    def locked(self):
        """屏幕是否已锁屏
        """
        return self.sesson.locked()

    def battery_info(self):
        """电池信息
        """
        return self.sesson.battery_info()

    def app_current(self):
        """当前app
        """
        return self.sesson.app_current()

    def set_clipboard(self, text):
        """设置剪贴板内容
        """
        self.sesson.set_clipboard(text)

    # def get_clipboard(self):  # Not working now
    #     return self.sesson.get_clipboard()

    def save_screenshot(self, destination):
        """保存截图
        """
        self.sesson.screenshot().save(destination)

    def deactivate(self, time):
        """停用app一段时间
        """
        self.sesson.deactivate(time)

    def window_size(self):
        """Get width and height
        """
        return self.sesson.window_size()

    def tap(self, x, y):
        self.sesson.tap(x, y)

    def click(self, x, y):
        self.sesson.click(x, y)

    def double_tap(self, x, y):
        self.sesson.double_tap(x, y)

    def swipe(self, x1, y1, x2, y2, duration=0):
        self.sesson.swipe(x1, y1, x2, y2, duration)

    def swipe_left(self):
        self.sesson.swipe_left()

    def swipe_right(self):
        self.sesson.swipe_right()

    def swipe_up(self):
        self.sesson.swipe_up()

    def swipe_down(self):
        self.sesson.swipe_down()

    def tap_hold(self, x, y, duration=0):
        self.sesson.tap_hold(x, y, duration)

    def keyboard_dismiss(self):
        self.sesson.keyboard_dismiss()
