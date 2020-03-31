#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2019/8/30 16:58
# @Author  : Kelvin.Ye
import os
from datetime import datetime
from enum import Enum, unique

from uiautomator2 import Device, Session
from uiautomator2.session import UiObject

from appuiautomator.exceptions import U2ClientError
from appuiautomator.utils import config
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


@unique
class By(Enum):
    """元素定位类型枚举类
    """
    timeout = 'timeout'
    text = 'text'
    textContains = 'textContains'
    textMatches = 'textMatches'
    textStartsWith = 'textStartsWith'
    className = 'className'
    classNameMatches = 'classNameMatches'
    description = 'description'
    descriptionContains = 'descriptionContains'
    descriptionMatches = 'descriptionMatches'
    descriptionStartsWit = 'descriptionStartsWit'
    checkable = 'checkable'
    checked = 'checked'
    clickable = 'clickable'
    longClickable = 'longClickable'
    scrollable = 'scrollable'
    enabled = 'enabled'
    focusable = 'focusable'
    focused = 'focused'
    selected = 'selected'
    packageName = 'packageName'
    packageNameMatches = 'packageNameMatches'
    resourceId = 'resourceId'
    resourceIdMatches = 'resourceIdMatches'
    index = 'index'
    instance = 'instance'
    xpath = 'xpath'
    innerElement = 'innerElement'
    allowScrollSearch = 'allow_scroll_search'


class Location:
    """元素定位信息类，主要用于将 By枚举转换为 str
    """

    @staticmethod
    def kwargs(location_dict) -> dict:
        kwargs = dict()
        for k, v in location_dict.items():
            if isinstance(k, By) and k != By.timeout:
                kwargs[k.value] = location_dict.get(k)
        return kwargs


class Element:
    """元素类，封装各种元素的操作
    """

    def __init__(self, d: Device(''),
                 location: dict = None,
                 ui_obj: UiObject = None,
                 timeout: int = None) -> None:
        """构造函数

        :param d:           uiautomator2.Device 实例对象
        :param location:    元素定位信息
        :param ui_obj:      UiObject 实例对象
        :param timeout:     超时时间
        """
        self._d = d
        if location is not None:
            self._element: UiObject = (
                d(**Location.kwargs(location)) if By.xpath not in location else d.xpath(location.get(By.xpath)))
        elif ui_obj is not None:
            self._element: UiObject = ui_obj
        else:
            raise U2ClientError('参数 location和 element不能同时为空')
        if location is not None and By.timeout in location:
            self._timeout = location.get(By.timeout)
        else:
            self._timeout = timeout

    def get_element(self) -> UiObject:
        return self._element

    def update_element(self, element: Session) -> None:
        self._element = element

    def child(self, location: dict) -> "Element":
        """查找子元素
        """
        return Element(self._d, ui_obj=self._element.child(**Location.kwargs(location)),
                       timeout=self._timeout if By.timeout not in location else location.get(By.timeout))

    def sibling(self, location: dict) -> "Element":
        """查找兄弟元素
        """
        return Element(self._d, ui_obj=self._element.sibling(**Location.kwargs(location)),
                       timeout=self._timeout if By.timeout not in location else location.get(By.timeout))

    def left(self, location: dict):
        """查找左元素
        """
        return Element(self._d, ui_obj=self._element.left(**Location.kwargs(location)),
                       timeout=self._timeout if By.timeout not in location else location.get(By.timeout))

    def right(self, location: dict):
        """查找右元素
        """
        return Element(self._d, ui_obj=self._element.right(**Location.kwargs(location)),
                       timeout=self._timeout if By.timeout not in location else location.get(By.timeout))

    def up(self, location: dict):
        """查找上元素
        """
        return Element(self._d, ui_obj=self._element.up(**Location.kwargs(location)),
                       timeout=self._timeout if By.timeout not in location else location.get(By.timeout))

    def down(self, location: dict):
        """查找下元素
        """
        return Element(self._d, ui_obj=self._element.down(**Location.kwargs(location)),
                       timeout=self._timeout if By.timeout not in location else location.get(By.timeout))

    @property
    def count(self):
        """元素个数
        """
        return self._element.count

    def __len__(self):
        return self._element.count

    def __getitem__(self, index):
        return Element(self._d, ui_obj=self._element[index], timeout=self._timeout)

    def __iter__(self):
        obj, length = self, self._element.count

        class Iter:
            def __init__(self):
                self.index = -1

            def next(self):
                self.index += 1
                if self.index < length:
                    return obj[self.index]
                else:
                    raise StopIteration()

            __next__ = next

        return Iter()

    def exists(self) -> bool:
        """判断元素是否存在
        """
        return self._element.exists(timeout=self._timeout)

    def info(self):
        """获取元素详细信息
        """
        return self._element.info()

    def click(self) -> None:
        """点击元素
        """
        self._element.click(timeout=self._timeout)

    def long_click(self, duration: int = None) -> None:
        """长点击元素
        """
        self._element.long_click(duration=duration, timeout=self._timeout)

    def get_text(self) -> str:
        """获取元素的文本
        """
        return self._element.get_text(timeout=self._timeout)

    def set_text(self, text: str) -> None:
        """设置元素的文本
        """
        self._element.set_text(text, timeout=self._timeout)

    def clear_text(self) -> None:
        """清除元素的文本
        """
        self._element.clear_text(timeout=self._timeout)

    def get_center_point(self):
        """获取元素中心点
        """
        self._element.center()

    def screenshot(self, save_uri: str = None) -> str:
        """元素级截图
        """
        element_info = self._element.info
        bounds = element_info.info.get('bounds')
        left = bounds.get('left')
        top = bounds.get('top')
        right = bounds.get('right')
        bottom = bounds.get('bottom')
        # 设备截图
        image = self._d.screenshot()
        # 截图剪裁
        cropped = image.crop((left, top, right, bottom))
        if not save_uri:
            save_uri = os.path.join(config.get_project_path(),
                                    'testcases', '.tmp',
                                    f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg')
        cropped.save(save_uri)
        log.info(f'保存元素截图至 {save_uri}')
        return save_uri
