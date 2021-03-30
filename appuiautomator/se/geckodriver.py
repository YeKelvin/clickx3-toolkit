#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : geckodriver.py
# @Time    : 2020/9/11 15:32
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from appuiautomator.se.driver_util import last_gecodriver_path, gecodriver_log_path
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)

UA_IPHONE_X = (
    r'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
    r'Version/12.0 Mobile/15A372 Safari/604.1'
)


def firefox_driver(exe_path=None,
                   log_path=None,
                   headless=False,
                   ua=None,
                   lang='zh-CN',
                   page_load_strategy='normal',
                   maximize=False):
    """

    :param exe_path:            driver路径
    :param log_path:            driver日志路径
    :param headless:            无头模式
    :param ua:                  user-agent
    :param lang:                浏览器语言，zh-CN | en-US | km-KH
    :param page_load_strategy:  页面加载策略，none | eager | normal
    :param maximize:            是否最大化窗口

    :return: WebDriver
    """
    option = webdriver.FirefoxOptions()
    option.headless = headless

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', lang)
    profile.set_preference('general.useragent.override', ua) if ua else None

    capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    capabilities['pageLoadStrategy'] = page_load_strategy

    wd = webdriver.Firefox(executable_path=exe_path or last_gecodriver_path(),
                           service_log_path=log_path or gecodriver_log_path(),
                           options=option,
                           firefox_profile=profile,
                           desired_capabilities=capabilities)

    if maximize:
        wd.maximize_window()

    atexit.register(wd.quit)  # always quit driver when done
    return wd
