#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
import time

from PIL import Image
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from appuiautomator.exceptions import PageElementError, PageSelectException
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

LOCATORS = {
    'id': By.ID,
    'class_name': By.CLASS_NAME,
    'name': By.NAME,
    'css': By.CSS_SELECTOR,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME
}


class Element:
    @property
    def location_info(self):
        return (
            f'Location:{[str(k) + "=" + str(v) for k, v in self.kwargs.items()]}, Description:{str(self.description)}'
        )

    def __init__(self, timeout=5, desc=None, **kwargs):
        self.timeout = timeout
        self.description = desc
        if not kwargs:
            raise ValueError('Please specify a locator')
        self.kwargs = kwargs
        if len(kwargs) > 1:
            raise ValueError('Please specify only one locator')
        self.k, self.v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATORS[self.k], self.v)
        except KeyError:
            raise PageElementError(f'Element positioning of type {self.k} is not supported. ')

    def get_element(self, context):
        try:
            element = context.find_element(*self.locator)
        except NoSuchElementException:
            return None
        else:
            try:
                style_red = 'arguments[0].style.border="2px solid red"'
                context.execute_script(style_red, element)
            except WebDriverException:
                return element
            return element

    def find(self, context):
        for i in range(1, self.timeout):
            element = self.get_element(context)
            if element is not None:
                return element
        raise NoSuchElementException()

    def __get__(self, instance, owner, context=None):
        if instance is None:
            return None
        context = instance.driver
        return self.find(context)

    def __set__(self, instance, value):
        element = self.__get__(instance, instance.__class__)
        element.send_keys(value)


class Elements(Element):
    def find(self, context):
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
            raise PageSelectException('"value" or "text" or "index" options can not be all empty.')


class ElUtil:
    @staticmethod
    def screenshot(wd, el, filename):
        while not bool(el.get_attribute('complete')):
            time.sleep(0.5)

        wd.save_screenshot('full-screenshot.png')
        left = el.location['x']
        top = el.location['y']
        right = el.location['x'] + el.size['width']
        bottom = el.location['y'] + el.size['height']
        im = Image.open('full-screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save(f'{filename}.png')
