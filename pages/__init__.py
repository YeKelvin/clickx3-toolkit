#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2019/8/30 17:00
# @Author  : Kelvin.Ye
from appuiautomator import MobileDevice, Element, DeviceType
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class BasePage:
    """页面基类
    """

    _android_elements: dict = None
    _ios_elements: dict = None
    _components: dict = None

    def __init__(self, d: MobileDevice) -> None:
        self._d = d
        # 初始化页面元素
        self.elements: {str, Element} = self.__create_element_foreach()
        # 初始化组件
        if self._components:
            self.components = {}
            for name, component_class in self._components.items():
                self.components[name] = component_class(self._d)

    def __create_element_foreach(self):
        """遍历创建元素对象
        """

        def create_element(d: MobileDevice, locations: dict):
            elements = {}
            for name, location in locations.items():
                elements[name] = Element(d.get_device(), location)
            return elements

        if self._d.type == 'Android':
            return create_element(self._d, self._android_elements)
        elif self._d.type == 'IOS':
            return create_element(self._d, self._ios_elements)


class BaseAPP:
    """App基类
    """
    package_name: str = None
    bundle_identifier: str = None

    def __init__(self, d: MobileDevice) -> None:
        self.d = d
        if self.d.type == DeviceType.ANDROID.value:
            self.app_name = self.package_name
        else:
            self.app_name = self.bundle_identifier

    def restart(self):
        """重启 app
        """
        self.d.app.stop(self.app_name)
        self.d.app.start(self.app_name)
        self.d.app.wait(self.app_name)

    def clear_cache(self):
        """清空 app缓存
        """
        self.d.app.stop(self.app_name)
        self.d.app.clear_cache(self.app_name)
        self.d.app.start(self.app_name)

    def switch_me(self):
        self.d.app.start(self.app_name)
