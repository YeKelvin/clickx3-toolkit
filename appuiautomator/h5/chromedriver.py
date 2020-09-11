#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : chromedriver
# @Time    : 2020/9/10 11:30
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from appuiautomator.h5.driver_util import last_chromedriver_path
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class ChromeDriver:
    def __init__(self, exe_path=None, u2d=None, headless=False, ua=None, lang='zh-CN', page_load_strategy='normal'):
        """

        Args:
            exe_path: driver路径
            u2d: uiautomator2实例
            headless: 无头模式
            ua: user-agent
            lang: 浏览器语言，zh-CN | en-US | km-KH
            page_load_strategy: 页面加载策略，none | eager | normal

        """
        self.u2d = u2d
        self.exe_path = exe_path

        self.options = webdriver.ChromeOptions()
        self.options.headless = headless
        self.options.set_capability('noRetest', True)

        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument(f'--lang={lang}')
        self.options.add_argument(f'--user-agent={ua}')

        prefs = {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False
        }
        self.options.add_experimental_option('prefs', prefs)

        self.capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        self.capabilities['pageLoadStrategy'] = page_load_strategy

    def driver(self):
        wd = webdriver.Chrome(executable_path=self.exe_path or last_chromedriver_path(),
                              chrome_options=self.options,
                              desired_capabilities=self.capabilities)

        atexit.register(wd.quit)  # always quit driver when done
        return wd

    def pc_h5_driver(self, deviceName='iPhone X'):
        self.options.add_experimental_option('mobileEmulation', {'deviceName': deviceName})
        wd = webdriver.Chrome(executable_path=self.exe_path or last_chromedriver_path(),
                              chrome_options=self.options,
                              desired_capabilities=self.capabilities)

        atexit.register(wd.quit)  # always quit driver when done
        return wd

    def android_h5_driver(self, package=None, attach=True, activity=None, process=None):
        app = self.u2d.app_current()
        self.options.add_experimental_option('androidDeviceSerial', self.u2d.serial)
        self.options.add_experimental_option('androidUseRunningApp', attach)
        self.options.add_experimental_option('androidPackage', package or app['package'])
        self.options.add_experimental_option('androidProcess', process or app['package'])
        self.options.add_experimental_option('androidActivity', activity or app['activity'])

        wd = webdriver.Chrome(executable_path=self.exe_path or last_chromedriver_path(),
                              chrome_options=self.options,
                              desired_capabilities=self.capabilities)

        atexit.register(wd.quit)  # always quit driver when done
        return wd
