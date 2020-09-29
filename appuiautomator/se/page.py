#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : page_object
# @Time    : 2020/4/3 11:56
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class Page:
    def __init__(self, driver, url=None):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(5)

    def run_script(self, js=None, *args):
        """run JavaScript script
        """
        if js is None:
            raise ValueError('Please input js script')
        else:
            self.driver.execute_script(js, *args)
