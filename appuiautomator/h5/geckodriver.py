#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : geckodriver
# @Time    : 2020/9/11 15:32
# @Author  : Kelvin.Ye
from selenium import webdriver

from appuiautomator.h5.driver_util import last_gecodriver_path
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

USER_AGENT_IPHONE_X = (
    r'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
    r'Version/12.0 Mobile/15A372 Safari/604.1'
)


class FirefoxDriver:
    def __init__(self, exe_path=None, headless=False, ua=None, lang='zh-CN', page_load_strategy='normal'):
        """

        Args:
            exe_path: driver路径
            headless: 无头模式
            ua: user-agent
            lang: 浏览器语言，zh-CN | en-US | km-KH
            page_load_strategy: 页面加载策略，none | eager | normal

        """
        self.exe_path = exe_path

        self.option = webdriver.FirefoxOptions()
        self.option.headless = headless

        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference('intl.accept_languages', lang)
        if ua:
            self.profile.set_preference('general.useragent.override', ua)

        self.capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        self.capabilities['pageLoadStrategy'] = page_load_strategy

    def driver(self):
        wd = webdriver.Firefox(executable_path=self.exe_path or last_gecodriver_path(),
                               firefox_profile=self.profile,
                               options=self.option,
                               desired_capabilities=self.capabilities)
        return wd
