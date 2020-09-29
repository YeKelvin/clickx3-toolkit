#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : element
# @Time    : 2020/9/29 15:47
# @Author  : Kelvin.Ye
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from appuiautomator.exceptions import PageElementError, PageSelectException
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

LOCATORS = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME
}


class Element:
    """Page Element descriptor.
    :param css:    `str`
        Use this css locator
    :param id_:    `str`
        Use this element ID locator
    :param name:    `str`
        Use this element name locator
    :param xpath:    `str`
        Use this xpath locator
    :param link_text:    `str`
        Use this link text locator
    :param partial_link_text:    `str`
        Use this partial link text locator
    :param tag:    `str`
        Use this tag name locator
    :param class_name:    `str`
        Use this class locator
    :param context: `bool`
        This element is expected to be called with context
    Page Elements are used to access elements on a page. The are constructed
    using this factory method to specify the locator for the element.
        >> from poium import Page, PageElement
        >> class MyPage(Page):
                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(name='bar', context=True)
    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """

    def __init__(self, context=False, timeout=4, log=False, describe="", **kwargs):
        self.time_out = timeout
        self.log = log
        self.describe = describe
        if not kwargs:
            raise ValueError('Please specify a locator')
        if len(kwargs) > 1:
            raise ValueError('Please specify only one locator')
        self.k, self.v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATORS[self.k], self.v)
        except KeyError:
            raise PageElementError(f'Element positioning of type {self.k} is not supported. ')
        self.has_context = bool(context)

    def get_element(self, context):
        try:
            element = context.find_element(*self.locator)
        except NoSuchElementException:
            return None
        else:
            try:
                style_red = 'arguments[0].style.border="2px solid red"'
                context.execute_script(style_red, element)
            except BaseException:
                return element
            return element

    def find(self, context):
        for i in range(1, self.time_out):
            if self.log is True:
                log.info(f'{self.describe}, {i} times search, {self.locator}')
            if self.get_element(context) is not None:
                return self.get_element(context)
        else:
            return self.get_element(context)

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            context = instance.driver

        return self.find(context)

    def __set__(self, instance, value):
        if self.has_context:
            raise PageElementError('Sorry, the set descriptor does not support elements with context.')
        element = self.__get__(instance, instance.__class__)
        if not element:
            raise PageElementError('Can not set value, element not found')
        element.send_keys(value)


class Elements(Element):
    """Like `PageElement` but returns multiple results.
    >> from page import Page, PageElements
    >> class MyPage(Page):
            all_table_rows = PageElements(tag='tr')
            elem2 = PageElement(id_='foo')
            elem_with_context = PageElement(tag='tr', context=True)
    """

    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise PageElementError('Sorry, the set descriptor does not support elements with context.')
        elements = self.__get__(instance, instance.__class__)
        if not elements:
            raise PageElementError('Can not set value, no elements found')
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


class PageWait:

    def __init__(self, element, timeout=3):
        """wait webelement display
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError('Type "timeout" error, must be type int()')

        for i in range(timeout_int):
            if element is not None:
                if element.is_displayed() is True:
                    break
                else:
                    sleep(1)
            else:
                sleep(1)
        else:
            raise TimeoutError('Timeout, element invisible')
