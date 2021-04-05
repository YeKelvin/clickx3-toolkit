#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
from functools import wraps
from time import sleep, time

from appuiautomator.exceptions import ElementException
from appuiautomator.utils.log_util import get_logger
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


def retry_find_webelement(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0]
        driver = parent.driver
        by = kwargs.pop('by', None) or args[1]
        value = kwargs.pop('value', None) or args[2]
        visible = kwargs.pop('visible', False)
        delay = kwargs.pop('timeout', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('timeout', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = func(parent, by, value)
            if visible:
                WebDriverWait(
                    driver, timeout
                ).until(
                    EC.visibility_of(element), message=f'By:[ {by} ] value:[ {value} ]'
                )
            return Element(driver=driver, web_element=element)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(interval)
                element = func(parent, by, value)
                if visible:
                    WebDriverWait(
                        driver, timeout
                    ).until(
                        EC.visibility_of(element), message=f'By:[ {by} ] value:[ {value} ]'
                    )
                return Element(driver=driver, web_element=element)
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

    return wrapper


def retry_find_webelements(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0]
        driver = parent.driver
        by = kwargs.pop('by', None) or args[1]
        value = kwargs.pop('value', None) or args[2]
        delay = kwargs.pop('timeout', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('timeout', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            elements = func(parent, by, value)
            if not elements:
                raise NoSuchElementException(f'By:[ {by} ] value:[ {value} ]')
            return Elements(driver=driver, web_elements=elements)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(interval)
            elements = func(parent, by, value)
            if not elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {by} ] value:[ {value} ]')
                continue
            return Elements(driver=driver, web_elements=elements)

    return wrapper


class Element(WebElement):
    def __init__(self,
                 by: By = None,
                 value: str = None,
                 visible: bool = True,
                 driver: WebDriver = None,
                 web_element: WebElement = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):
        if driver:
            self.driver = driver
        if web_element:
            # 直接把WebElement的属性字典复制过来
            self.__dict__.update(web_element.__dict__)
        self.by = by
        self.value = value
        self.visible = visible
        self.delay = delay
        self.timeout = timeout
        self.interval = interval

    def __find(self):
        if (not self.by) or (not self.value):
            raise ElementException('元素定位信息不允许为空')

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
            if self.visible:
                WebDriverWait(
                    self.driver, self.timeout
                ).until(
                    EC.visibility_of(self), message=f'By:[ {self.by} ] value:[ {self.value} ]'
                )
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(self.interval)
                element = self.__find()
                self.__dict__.update(element.__dict__)
                if self.visible:
                    WebDriverWait(
                        self.driver, self.timeout
                    ).until(
                        EC.visibility_of(self), message=f'By:[ {self.by} ] value:[ {self.value} ]'
                    )
                return self
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')

        browser = getattr(instance, 'browser', None)
        webview = getattr(instance, 'webview', None)
        if (browser is None) and (webview is None):
            raise ElementException('instance必须包含browser或webview属性的其中之一')

        container = browser or webview

        driver = getattr(container, 'driver', None)
        if driver is None:
            raise ElementException('browser或webview必须包含driver属性')

        self.driver = driver
        return self.__retry_find()

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实send_keys()吧')

    @retry_find_webelement
    def find_element(self, by, value, **kwargs):
        """查找元素

        Args:
            by(By): 定位类型
            value(str): 定位值
            visible(bool): 是否等待可见，default=False
            delay(float): 延迟时间，default=0.5
            timeout(float): 查找超时时间，default=10
            interval(float): 重试查找间隔时间，default=0.5

        Returns:
            Element
        """
        return super().find_element(by, value)

    @retry_find_webelements
    def find_elements(self, by, value, **kwargs):
        """查找元素

        Args:
            by(By): 定位类型
            value(str): 定位值
            delay(float): 延迟时间，default=0.5
            timeout(float): 查找超时时间，default=10
            interval(float): 重试查找间隔时间，default=0.5

        Returns:
            Elements
        """
        return super().find_elements(by, value)

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


class Elements(list):

    @property
    def count(self):
        return len(self)

    def __init__(self,
                 by: By = None,
                 value: str = None,
                 driver: WebDriver = None,
                 web_elements: list = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):
        if driver:
            self.driver = driver
        if web_elements:
            self.extend(web_elements)
        self.by = by
        self.value = value
        self.delay = delay
        self.timeout = timeout
        self.interval = interval

    def __find(self):
        if (not self.by) or (not self.value):
            raise ElementException('元素定位信息不允许为空')

        return self.driver.find_elements(self.by, self.value)

    def __retry_find(self):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            elements = self.__find()
            if not elements:
                raise NoSuchElementException(f'By:[ {self.by} ] value:[ {self.value} ]')
            self.extend(elements)
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            elements = self.__find()
            if not elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {self.by} ] value:[ {self.value} ]')
                continue
            self.extend(elements)
            return self

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

    def __getitem__(self, index: int):
        item = super().__getitem__(index)
        if isinstance(item, Element):
            return item
        elif isinstance(item, WebElement):
            return Element(driver=self.driver, web_element=item)
        else:
            raise ElementException(f'仅支持uitesttoolkit.Element和selenium.WebElement，object:[ {item} ]')
