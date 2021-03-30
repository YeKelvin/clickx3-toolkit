#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
import io
from functools import wraps
from time import sleep, time

from appuiautomator.exceptions import ElementException
from appuiautomator.utils.log_util import get_logger
from PIL import Image
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

log = get_logger(__name__)


class Locator:
    def __init__(self, by: By, value: str):
        self.by = by
        self.value = value


def _retry(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        self = args[0]
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = func(*args, **kwargs)
            return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of(element))

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(self.interval)
                element = func(*args, **kwargs)
                return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of(element))
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue
    return wrapped_function


class Element(WebElement):
    def __init__(self,
                 by: By = None,
                 value: str = None,
                 driver: WebDriver = None,
                 web_element: WebElement = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5,
                 return_list: bool = False):
        if driver:
            self.driver = driver

        if web_element:
            # 直接把WebElement的属性字典复制过来
            self.__dict__ = web_element.__dict__

        self.by = by
        self.value = value
        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.return_list = return_list

    def __find(self):
        if (not self.by) or (not self.value):
            raise ElementException('元素定位信息不允许为空')

        if self.return_list:
            return self.driver.find_elements(self.by, self.value)
        else:
            return self.driver.find_element(self.by, self.value)

    def __retry_find(self):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = self.__find()
            self.__dict__.update(element.__dict__)
            return self.__wait_until_visible()

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(self.interval)
                element = self.__find()
                self.__dict__.update(element.__dict__)
                return self.__wait_until_visible()
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

    def __wait_until_visible(self):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of(self))

    def __getitem__(self, index: int):
        return Element(self[index])

    @property
    def count(self):
        return len(self)

    def __iter__(self):
        obj, length = self, self.count

        class Iter(object):
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

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')

        browser = getattr(instance, 'browser', None)
        if browser is None:
            raise ElementException('instance必须包含browser属性')

        driver = getattr(instance.browser, 'driver', None)
        if driver is None:
            raise ElementException('instance.browser必须包含driver属性')

        self.driver = driver
        return self.__retry_find()

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实send_keys()吧')

    @_retry
    def find_element(self, by, value):
        return Element(super().find_element(by, value))

    @_retry
    def find_elements(self, by, value):
        return Element(super().find_elements(by, value))

    def save_screenshot(self, filename, frequency=0.5):
        """保存元素截图

        :param filename:  截图名称
        :param frequency: 读取图片complete属性的频率
        :return:
        """
        end_time = time() + self.timeout

        while not bool(self.get_attribute('complete')):
            sleep(frequency)
            if time() > end_time:
                raise TimeoutException('CONTENT:Image loading is not complete')

        return self.screenshot(filename)

    def select_by_value(self, value):
        """Selenium Select API"""
        Select(self).select_by_value(value)

    def select_by_visible_text(self, text):
        """Selenium Select API"""
        Select(self).select_by_visible_text(text)

    def select_by_index(self, index):
        """Selenium Select API"""
        Select(self).select_by_index(index)

    def move_here(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).move_to_element(self).perform()

    def click_and_hold(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).click_and_hold(self).perform()

    def double_click(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).double_click(self).perform()

    def context_click(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).context_click(self).perform()

    def drag_and_drop_by_offset(self, x, y):
        """Selenium ActionChains API"""
        ActionChains(self.driver).drag_and_drop_by_offset(self, xoffset=x, yoffset=y).perform()


class ElementUtil:
    @staticmethod
    def screenshot(wd, el, path):
        while not bool(el.get_attribute('complete')):
            sleep(0.5)

        full_screenshot_buff = io.BytesIO(wd.driver.get_screenshot_as_png())
        left = el.location['x']
        top = el.location['y']
        right = left + el.size['width']
        bottom = top + el.size['height']
        im = Image.open(full_screenshot_buff)
        im = im.crop((left, top, right, bottom))
        im.save(path)
