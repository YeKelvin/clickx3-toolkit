#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : chromedriver
# @Time    : 2020/9/10 11:30
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from appuiautomator.se.driver_util import last_chromedriver_path, chromedriver_log_path
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


def chrome_driver(exe_path=None, device_name=None, headless=False, ua=None, lang='zh-CN',
                  page_load_strategy='normal'):
    """

    Args:
        exe_path: driver路径
        device_name: uiautomator2实例
        headless: 无头模式
        ua: user-agent
        lang: 浏览器语言，zh-CN | en-US | km-KH
        page_load_strategy: 页面加载策略，none | eager | normal

    """
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.set_capability('noRetest', True)

    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-popup-blocking')
    options.add_argument(f'--lang={lang}')
    options.add_argument(f'--user-agent={ua}')

    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    })
    options.add_experimental_option('mobileEmulation', {'deviceName': device_name} if device_name else None)

    capabilities = webdriver.DesiredCapabilities.CHROME.copy().update({
        'pageLoadStrategy': page_load_strategy
    })
    wd = webdriver.Chrome(executable_path=exe_path or last_chromedriver_path(),
                          service_log_path=chromedriver_log_path(),
                          chrome_options=exe_path,
                          desired_capabilities=capabilities)

    atexit.register(wd.quit)  # always quit driver when done
    return wd


def webview_driver(device, exe_path=None, package=None, attach=True, activity=None, process=None, lang='zh-CN',
                   page_load_strategy='normal'):
    app = device.app_current()
    options = webdriver.ChromeOptions()
    options.add_argument(f'--lang={lang}')
    options.add_experimental_option('androidDeviceSerial', device.serial)
    options.add_experimental_option('androidUseRunningApp', attach)
    options.add_experimental_option('androidPackage', package or app['package'])
    options.add_experimental_option('androidProcess', process or app['package'])
    options.add_experimental_option('androidActivity', activity or app['activity'])

    capabilities = webdriver.DesiredCapabilities.CHROME.copy().update({
        'pageLoadStrategy': page_load_strategy
    })

    wd = webdriver.Chrome(executable_path=exe_path or last_chromedriver_path(),
                          service_log_path=chromedriver_log_path(),
                          chrome_options=options,
                          desired_capabilities=capabilities)

    atexit.register(wd.quit)  # always quit driver when done
    return wd
