#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : webdriver.py
# @Time    : 2020/10/14 12:24
# @Author  : Kelvin.Ye
import io
import os
import time

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image


class Browser:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute_script(self, js=None, *args):
        """Execute JavaScript scripts.
        """
        if js is None:
            raise ValueError('Please input js script')

        return self.driver.execute_script(js, *args)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = f'window.scrollTo({str(width)},{str(height)});'
        self.execute_script(js)

    def get_title(self):
        """
        JavaScript API
        Get page title.
        """
        js = 'return document.title;'
        return self.execute_script(js)

    def get_url(self):
        """
        JavaScript API
        Get page URL.
        """
        js = "return document.URL;"
        return self.execute_script(js)

    def screenshots(self, path=None, filename=None):
        """
        selenium API
        Saves a screenshots of the current window to a PNG image file
        :param path: The path to save the file
        :param filename: The file name
        """
        if path is None:
            path = os.getcwd()
        if filename is None:
            filename = str(time.time()).split(".")[0] + ".png"
        file_path = os.path.join(path, filename)
        self.driver.save_screenshot(file_path)

    def accept_alert(self):
        """
        selenium API
        Accept warning box.
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        selenium API
        Dismisses the alert available.
        """
        self.driver.switch_to.alert.dismiss()

    def alert_is_display(self):
        """
        selenium API
        Determines if alert is displayed
        """
        try:
            self.driver.switch_to.alert
        except NoAlertPresentException:
            return False
        else:
            return True

    def get_alert_text(self):
        """
        selenium API
        Get warning box prompt information.
        """
        return self.driver.switch_to.alert.text

    def move_by_offset(self, x, y):
        """
        selenium API
        Moving the mouse to an offset from current mouse position.

        :Args:
         - x: X offset to move to, as a positive or negative integer.
         - y: Y offset to move to, as a positive or negative integer.
        """
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def release(self):
        """
        selenium API
        Releasing a held mouse button on an element.
        """
        ActionChains(self.driver).release().perform()

    def move_to_element(self, element, index=None):
        ActionChains(self.driver).move_to_element(element).perform()

    def click_and_hold(self, element, index=None):
        ActionChains(self.driver).click_and_hold(element).perform()

    def double_click(self, element, index=None):
        ActionChains(self.driver).double_click(element).perform()

    def context_click(self, element, index=None):
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop_by_offset(self, element, x, y, index=None):
        ActionChains(self.driver).drag_and_drop_by_offset(element, xoffset=x, yoffset=y).perform()

    def screenshot_element(self, element, path:str, index=None):
        while not bool(element.get_attribute('complete')):
            time.sleep(0.5)

        full_screenshot_png = self.driver.get_screenshot_as_png()
        buff = io.BytesIO(full_screenshot_png)
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        image = Image.open(buff)
        image = image.crop((left, top, right, bottom))
        image.save(path)
