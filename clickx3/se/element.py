#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element.py
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
from functools import wraps
from time import sleep

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from clickx3.common.exceptions import ElementException
from clickx3.se.driver import Driver
from clickx3.se.support import expected_conditions as X3_EC
from clickx3.utils.log_util import get_logger


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
        driver = parent.driver  # type: Driver
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
                element.wait_until.visibility()
            return element

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(interval)
                web_element = func(parent, by, value)
                element = Element(driver=driver, web_element=web_element)
                if visible:
                    element.wait_until.visibility()
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
        driver = parent.driver  # type: Driver
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
    def __init__(
        self,
        by: By = None,
        value: str = None,
        visible: bool = True,
        driver: Driver = None,
        web_element: WebElement = None,
        delay: float = 0.5,
        timeout: float = 10,
        interval: float = 0.5
    ):

        if web_element:
            # 直接把WebElement的属性字典复制过来
            self.__dict__.update(web_element.__dict__)

        self._by = by
        self._value = value
        self._visible = visible
        self._delay = delay
        self._timeout = timeout
        self._interval = interval
        self.driver = driver
        self.wait_until = ElementWait(self)

    def __retry_find(self):
        if (not self._by) or (not self._value):
            raise ElementException('元素定位信息不允许为空')

        # 计算重试次数
        retry_count = int(float(self._timeout) / float(self._interval))
        # 延迟查找元素
        if self._delay:
            sleep(self._delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = self.driver.find_element(self._by, self._value)
            self.__dict__.update(element.__dict__)
            if self._visible:
                self.wait_until.visibility()
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(self._interval)
                element = self.driver.find_element(self._by, self._value)
                self.__dict__.update(element.__dict__)
                if self._visible:
                    self.wait_until.visibility()
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
            visible(bool, False): 是否等待可见
            delay(float, 0.5): 延迟时间
            timeout(float, 10): 查找超时时间
            interval(float, 0.5): 重试查找间隔时间

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
            delay(float, 0.5): 延迟时间
            timeout(float, 10): 查找超时时间
            interval(float, 0.5): 重试查找间隔时间

        Returns:
            Elements
        """
        return super().find_elements(by, value)

    def get_value(self):
        """获取元素的value属性值"""
        return self.get_attribute('value')

    def set_value(self, value):
        """修改元素的value属性值"""
        self.driver.execute_script(f'arguments[0].value="{value}";', self)

    def save_image(self, image_path):
        """保存图片，用于<img>元素

        Args:
            image_path (str): 图片保存路径
        """
        self.wait_until.image_completed()
        self.screenshot(image_path)

    def select_by_value(self, value):
        """Selenium Select API"""
        Select(self).select_by_value(value)

    def select_by_visible_text(self, text):
        """Selenium Select API"""
        Select(self).select_by_visible_text(text)

    def select_by_index(self, index):
        """Selenium Select API"""
        Select(self).select_by_index(index)

    def select_by_text_contains(self, text):
        """Selenium Select API"""
        options = Select(self).options
        for option in options:
            if not option.is_enabled():
                continue
            if text in option.text:
                if not option.is_selected():
                    option.click()
                return
        raise ElementException(f'无匹配的选项或无可选择的选项，text:[ {text} ]')

    def select_by_text_not_contains(self, text):
        """Selenium Select API"""
        options = Select(self).options
        for option in options:
            if not option.is_enabled():
                continue
            if text not in option.text:
                if not option.is_selected():
                    option.click()
                return
        raise ElementException(f'无匹配的选项或无可选择的选项，text:[ {text} ]')

    def move_here(self, after_sleep=0.5):
        """Selenium ActionChains API"""
        ActionChains(self.driver).move_to_element(self).perform()
        if after_sleep:
            sleep(after_sleep)

    def click(self):
        """
        Selenium API
        如果原生点击报错抛ElementNotInteractableException时，尝试使用坐标点击
        如果原生点击报错抛ElementClickInterceptedException时，尝试使用js点击
        """
        try:
            super().click()
        except ElementNotInteractableException:
            self.click_by_location()
        except ElementClickInterceptedException:
            self.click_by_js()

    def click_by_location(self):
        """点击元素的坐标"""
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
        """
        JavaScript API
        隐藏元素
        """
        js = "arguments[0].style.display='none';"
        self.driver.execute_script(js, self)

    def scroll_into_view(self):
        """
        JavaScript API
        滚动至元素
        """
        js = 'arguments[0].scrollIntoView(true);'
        self.driver.execute_script(js, self)

    def click_by_js(self):
        """
        JavaScript API
        js点击元素
        """
        js = 'arguments[0].click();'
        self.driver.execute_script(js, self)

    def highlight(self):
        """
        JavaScript API
        高亮元素
        """
        js = 'arguments[0].style.border="2px solid red";'
        self.driver.execute_script(js, self)


class Elements(list):

    @property
    def count(self):
        return len(self)

    def __init__(
        self,
        by: By = None,
        value: str = None,
        driver: Driver = None,
        web_elements: list = None,
        delay: float = 0.5,
        timeout: float = 10,
        interval: float = 0.5
    ):

        if web_elements:
            self.extend(web_elements)

        self._by = by
        self._value = value
        self._delay = delay
        self._timeout = timeout
        self._interval = interval
        self.driver = driver

    def __retry_find(self):
        if (not self._by) or (not self._value):
            raise ElementException('元素定位信息不允许为空')

        # 计算重试次数
        retry_count = int(float(self._timeout) / float(self._interval))
        # 延迟查找元素
        if self._delay:
            sleep(self._delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            elements = self.driver.find_elements(self._by, self._value)
            if not elements:
                raise NoSuchElementException(f'By:[ {self._by} ] value:[ {self._value} ]')
            self.extend(elements)
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self._interval)
            elements = self.driver.find_elements(self._by, self._value)
            if not elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {self._by} ] value:[ {self._value} ]')
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
            raise TypeError(f'仅支持clickx3.Element和selenium.WebElement，object:[ {item} ]')


class ElementWait:

    def __init__(self, element=None):
        self.element = element

    def _selector_to_str(self, errmsg):
        errmsg = f'errmsg:[ {errmsg} ] ' if errmsg else ''
        return errmsg + f'by:[ {self.element._by} ] value:[ {self.element._value} ]'

    def _wait_until(self, method, timeout, errmsg):
        errmsg = self._selector_to_str(errmsg)
        timeout = timeout or self.element._timeout
        return WebDriverWait(self.element.driver, timeout).until(method, message=errmsg)

    def visibility(self, timeout=None, errmsg=None):
        return self._wait_until(EC.visibility_of(self.element), timeout, errmsg)

    def invisibility(self, timeout=None, errmsg=None):
        log.info('等待元素不可见')
        return self._wait_until(EC.invisibility_of_element(self.element), timeout, errmsg)

    def clickable(self, timeout=None, errmsg=None):
        return self._wait_until(X3_EC.clickable_of(self.element), timeout, errmsg)

    def image_completed(self, timeout=None, errmsg=None):
        log.info('等待img图片加载完成')
        return self._wait_until(X3_EC.image_completed_of(self.element), timeout, errmsg)

    def text_contains(self, expected, refresh=False, timeout=None, errmsg=None):
        log.info(f'等待元素text包含:[ {expected} ]')
        try:
            return self._wait_until(X3_EC.text_contains_of(self.element, expected, refresh), timeout, errmsg)
        except TimeoutException:
            log.error(f'等待超时，当前元素text:[ {self.element.text} ]')
            raise
