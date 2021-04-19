#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
from functools import wraps
from time import sleep, time

from clickx3.exceptions import ElementException
from clickx3.utils.log_util import get_logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

log = get_logger(__name__)


class Locator(list):
    def __init__(self, by: By, value: str):
        self.by = by
        self.value = value
        self.append(by)
        self.append(value)


def retry_find_webelement(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0]
        driver = parent.driver  # type: WebDriver
        by = kwargs.pop('by', None) or args[1]
        value = kwargs.pop('value', None) or args[2]
        visible = kwargs.pop('visible', False)
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            web_element = func(parent, by, value)
            element = Element(driver=driver, web_element=web_element)
            if visible:
                element.wait.visibility()
            return element

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(interval)
                web_element = func(parent, by, value)
                element = Element(driver=driver, web_element=web_element)
                if visible:
                    element.wait.visibility()
                return element
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

    return wrapper


def retry_find_webelements(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0]
        driver = parent.driver  # type: WebDriver
        by = kwargs.pop('by', None) or args[1]
        value = kwargs.pop('value', None) or args[2]
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            web_elements = func(parent, by, value)
            if not web_elements:
                raise NoSuchElementException(f'By:[ {by} ] value:[ {value} ]')
            return Elements(driver=driver, web_elements=web_elements)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(interval)
            web_elements = func(parent, by, value)
            if not web_elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {by} ] value:[ {value} ]')
                continue
            return Elements(driver=driver, web_elements=web_elements)

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

        if web_element:
            # 直接把WebElement的属性字典复制过来
            self.__dict__.update(web_element.__dict__)

        self.driver = driver
        self.by = by
        self.value = value
        self.visible = visible
        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.wait = ElementWait(self)

    def __retry_find(self):
        if (not self.by) or (not self.value):
            raise ElementException('元素定位信息不允许为空')

        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = self.driver.find_element(self.by, self.value)
            self.__dict__.update(element.__dict__)
            if self.visible:
                self.wait.visibility()
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(self.interval)
                element = self.driver.find_element(self.by, self.value)
                self.__dict__.update(element.__dict__)
                if self.visible:
                    self.wait.visibility()
                return self
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')

        self.driver = instance.driver
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

    def textarea_value(self):
        """获取textarea元素的值"""
        return self.get_attribute('value')

    def save_screenshot(self, filename, frequency=0.5):
        """元素截图并保存

        Args:
            filename (str): 截图图片名称
            frequency (float): 判断图片complete属性的频率

        Raises:
            TimeoutException: [description]

        Returns:
            True | False
        """
        end_time = time() + self.timeout

        while not bool(self.get_attribute('complete')):
            sleep(frequency)
            if time() > end_time:
                raise TimeoutException('image loading is not complete')

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

    def move_here(self, after_sleep=0.5):
        """Selenium ActionChains API"""
        ActionChains(self.driver).move_to_element(self).perform()
        if after_sleep:
            sleep(after_sleep)

    def click(self, clickable=True):
        if clickable:
            self.wait.to_be_clickable()
        super().click()

    def click_by_location(self):
        size = self.size
        height = int(size['height']) / 2
        width = int(size['width']) / 2
        ActionChains(self.driver).move_to_element_with_offset(self, width, height).click().perform()

    def click_and_hold(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).click_and_hold(self).perform()

    def double_click(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).double_click(self).perform()

    def context_click(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).context_click(self).perform()

    def drag_and_drop_by_offset(self, xoffset, yoffset):
        """Selenium ActionChains API"""
        ActionChains(self.driver).drag_and_drop_by_offset(self, xoffset, yoffset).perform()

    def tap(self, center=True):
        """
        Selenium TouchActions API
        webview专用，单次点触，触控坐标为元素的左上角
        """
        if center:
            self.tap_center()
        else:
            TouchActions(self.driver).tap(self).perform()

    def tap_offset(self, xoffset, yoffset):
        """
        Selenium TouchActions API
        webview专用，单次点触，触控坐标是元素的左上角+偏移量

        Args:
            xoffset (int): x轴偏移量
            yoffset (int): y轴偏移量
        """
        location = self.location
        xcoord = int(location['x']) + int(xoffset)
        ycoord = int(location['y']) + int(yoffset)
        TouchActions(self.driver).tap_and_hold(xcoord, ycoord).release(xcoord, ycoord).perform()

    def tap_center(self):
        """
        Selenium TouchActions API
        webview专用，单次点触，触控坐标为元素的正中间
        """
        size = self.size
        height = int(size['height']) / 2
        width = int(size['width']) / 2
        self.tap_offset(width, height)

    def scroll_here(self):
        TouchActions(self.driver).scroll_from_element(self, 0, self.size['height']).perform()

    def hide(self):
        js = "arguments[0].style.display='none';"
        self.driver.execute_script(js, self)

    def scroll_into_view(self):
        js = 'arguments[0].scrollIntoView(true);'
        self.driver.execute_script(js, self)

    def click_by_js(self):
        js = 'arguments[0].click();'
        self.driver.execute_script(js, self)

    def highlight(self):
        js = 'arguments[0].style.border="2px solid red";'
        self.driver.execute_script(js, self)


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

    def __retry_find(self):
        if (not self.by) or (not self.value):
            raise ElementException('元素定位信息不允许为空')

        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            elements = self.driver.find_elements(self.by, self.value)
            if not elements:
                raise NoSuchElementException(f'By:[ {self.by} ] value:[ {self.value} ]')
            self.extend(elements)
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            elements = self.driver.find_elements(self.by, self.value)
            if not elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {self.by} ] value:[ {self.value} ]')
                continue
            self.extend(elements)
            return self

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')

        self.driver = instance.driver
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
            raise ElementException(f'仅支持clickx3.Element和selenium.WebElement，object:[ {item} ]')


class ElementWait:
    def __init__(self, element=None):
        self.element = element

    def visibility(self, timeout=None, message=None):
        if not message:
            message = f'By:[ {self.element.by} ] value:[ {self.element.value} ]'
        if not timeout:
            timeout = self.element.timeout
        return WebDriverWait(self.element.driver, timeout).until(EC.visibility_of(self.element), message=message)

    def invisibility(self, timeout=None, message=None):
        if not message:
            message = f'By:[ {self.element.by} ] value:[ {self.element.value} ]'
        if not timeout:
            timeout = self.element.timeout
        return WebDriverWait(self.element.driver, timeout).until(EC.invisibility_of_element(self.element), message=message)

    def to_be_clickable(self, timeout=None, message=None):
        if not message:
            message = f'By:[ {self.element.by} ] value:[ {self.element.value} ]'
        if not timeout:
            timeout = self.element.timeout
        return WebDriverWait(self.element.driver, timeout).until(EC.element_to_be_clickable(self.element), message=message)
