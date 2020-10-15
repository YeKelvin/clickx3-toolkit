#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
import io
import time
from typing import Optional

from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from appuiautomator.exceptions import ElementException, ElementNotFoundException
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

LOCATORS = {
    'id': By.ID,
    'name': By.NAME,
    'class_name': By.CLASS_NAME,
    'tag_name': By.TAG_NAME,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'css_selector': By.CSS_SELECTOR,
    'xpath': By.XPATH
}


class Element:
    @property
    def location_info(self):
        return (
            f'Location:{[str(k) + "=" + str(v) for k, v in self.kwargs.items()]}, Description:{str(self.description)}'
        )

    def __init__(self, timeout=5, desc=None, index=0, **kwargs):
        if not kwargs:
            raise ValueError('CONTENT:Please specify a locator')
        if len(kwargs) > 1:
            raise ValueError('CONTENT:Please specify only one locator')
        for by in kwargs.keys():
            if by not in LOCATORS:
                raise KeyError(f'CONTENT:Element positioning of type is not supported, OBJECT(by={by})')

        self.driver = None  # type: Optional[WebDriver]
        self.timeout = timeout
        self.description = desc
        self.index = index
        self.kwargs = kwargs
        self.by, self.value = next(iter(kwargs.items()))

    def __get_element(self) -> WebElement:
        elements = self.driver.find_elements(LOCATORS[self.by], self.value)
        if elements:
            try:
                element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of(elements[self.index]))
                return element
            except TimeoutException:
                raise ElementNotFoundException(self.location_info)
        raise ElementNotFoundException(self.location_info)

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException(f'CONTENT:The instance cannot be None')
        if not hasattr(instance, 'browser'):
            raise ElementException(
                f'CONTENT:The owner instance must have the browser attribute, OBJECT(instance={instance})')
        if not hasattr(instance.browser, 'driver'):
            raise ElementException(
                f'CONTENT:The browser must have the driver attribute, OBJECT(browser={instance.browser} )')

        if self.driver is None:
            self.driver = instance.browser.driver
        return self

    def __set__(self, instance, value):
        self.__get_element().send_keys(value)

    @property
    def parent(self):
        """Selenium API"""
        return self.__get_element().parent

    @property
    def id(self):
        """Selenium API"""
        return self.__get_element().id

    @property
    def tag_name(self):
        """Selenium API"""
        return self.__get_element().tag_name

    @property
    def text(self):
        """Selenium API"""
        return self.__get_element().text

    @property
    def size(self):
        """Selenium API"""
        return self.__get_element().size

    @property
    def location(self):
        """Selenium API"""
        return self.__get_element().location

    @property
    def location_once_scrolled_into_view(self):
        """Selenium API"""
        return self.__get_element().location_once_scrolled_into_view

    @property
    def rect(self):
        """Selenium API"""
        return self.__get_element().rect

    def send_keys(self, *value):
        """Selenium API"""
        self.__get_element().send_keys(*value)

    def click(self):
        """Selenium API"""
        self.__get_element().click()

    def submit(self):
        """Selenium API"""
        self.__get_element().submit()

    def clear(self):
        """Selenium API"""
        self.__get_element().clear()

    def get_property(self, name):
        """Selenium API"""
        return self.__get_element().get_property(name)

    def get_attribute(self, name):
        """Selenium API"""
        return self.__get_element().get_attribute(name)

    def is_selected(self):
        """Selenium API"""
        return self.__get_element().is_selected()

    def is_enabled(self):
        """Selenium API"""
        return self.__get_element().is_enabled()

    def is_displayed(self):
        """Selenium API"""
        return self.__get_element().is_displayed()

    def value_of_css_property(self, property_name):
        """Selenium API"""
        return self.__get_element().value_of_css_property(property_name)

    def save_screenshot(self, filename, frequency=0.5):
        """保存元素截图

        :param filename:  截图名称
        :param frequency: 读取图片complete属性的频率
        :return:
        """
        element = self.__get_element()
        end_time = time.time() + self.timeout

        while not bool(element.get_attribute('complete')):
            time.sleep(frequency)
            if time.time() > end_time:
                raise TimeoutException('CONTENT:Image loading is not complete')

        return self.__get_element().screenshot(filename)

    def select_by_value(self, value):
        """Selenium Select API"""
        element = self.__get_element()
        Select(element).select_by_value(value)

    def select_by_visible_text(self, text):
        """Selenium Select API"""
        element = self.__get_element()
        Select(element).select_by_visible_text(text)

    def select_by_index(self, index):
        """Selenium Select API"""
        element = self.__get_element()
        Select(element).select_by_index(index)

    def move_here(self):
        """Selenium ActionChains API"""
        element = self.__get_element()
        ActionChains(self.driver).move_to_element(element).perform()

    def click_and_hold(self):
        """Selenium ActionChains API"""
        element = self.__get_element()
        ActionChains(self.driver).click_and_hold(element).perform()

    def double_click(self):
        """Selenium ActionChains API"""
        element = self.__get_element()
        ActionChains(self.driver).double_click(element).perform()

    def context_click(self):
        """Selenium ActionChains API"""
        element = self.__get_element()
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop_by_offset(self, x, y):
        """Selenium ActionChains API"""
        element = self.__get_element()
        ActionChains(self.driver).drag_and_drop_by_offset(element, xoffset=x, yoffset=y).perform()


class ElementUtil:
    @staticmethod
    def screenshot(wd, el, path):
        while not bool(el.get_attribute('complete')):
            time.sleep(0.5)

        full_screenshot_buff = io.BytesIO(wd.driver.get_screenshot_as_png())
        left = el.location['x']
        top = el.location['y']
        right = left + el.size['width']
        bottom = top + el.size['height']
        im = Image.open(full_screenshot_buff)
        im = im.crop((left, top, right, bottom))
        im.save(path)
