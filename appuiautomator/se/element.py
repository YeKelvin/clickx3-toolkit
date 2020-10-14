#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
import time
from typing import Optional, Union, List

from PIL import Image
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from appuiautomator.exceptions import ElementException, SelectElementException, ElementNotFoundException
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

    def __init__(self, timeout=5, desc=None, **kwargs):
        if not kwargs:
            raise ValueError('❌ Please specify a locator')
        if len(kwargs) > 1:
            raise ValueError('❌ Please specify only one locator')

        self.timeout = timeout
        self.description = desc
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        try:
            self.locator = (LOCATORS[self.k], self.v)
        except KeyError:
            raise ElementException(f'❌ Element positioning of type {self.k} is not supported')

    def __find(self, context) -> Optional[WebElement]:
        """

        :param context: selenium.webdriver.remote.webdriver.WebDriver
        :return:
        """
        try:
            if self.timeout:
                element = WebDriverWait(context, self.timeout).until(EC.visibility_of_element_located(self.locator))
                if element:
                    return element
        except TimeoutException:
            raise ElementNotFoundException(f'Element not found. {self.location_info}')

    def __get__(self, instance, owner) -> Union[List[WebElement], WebElement, None]:
        if instance is None:
            return None
        if not hasattr(instance, 'driver'):
            raise ElementException(f'The owner instance {instance} must have the driver attribute')

        return self.__find(instance.driver)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise ElementNotFoundException(f'Cannot set value, element not found. {self.location_info}')
        element.send_keys(value)


class Elements(Element):
    def __find(self, context) -> List[WebElement]:
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        elements = self.__get__(instance, instance.__class__)
        [element.send_keys(value) for element in elements]


class SelectElement:
    """
    Processing select drop-down selection box
    """

    def __init__(self, select_element, value=None, text=None, index=None):
        if value is not None:
            Select(select_element).select_by_value(value)
        elif text is not None:
            Select(select_element).select_by_visible_text(text)
        elif index is not None:
            Select(select_element).select_by_index(index)
        else:
            raise SelectElementException('"value" or "text" or "index" options cannot be empty at the same time')


class ElementUtil:
    @staticmethod
    def screenshot(wd, el, path):
        while not bool(el.get_attribute('complete')):
            time.sleep(0.5)

        wd.save_screenshot('full-screenshot.png')
        left = el.location['x']
        top = el.location['y']
        right = el.location['x'] + el.size['width']
        bottom = el.location['y'] + el.size['height']
        im = Image.open('full-screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save(f'{path}.png')
