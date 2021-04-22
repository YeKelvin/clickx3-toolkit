#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : chromedriver.py
# @Time    : 2020/9/10 11:30
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from clickx3.se.support.driver_util import chromedriver_last_version_path, chromedriver_log_path
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


def chrome_driver(driver_path=None,
                  device_name=None,
                  headless=False,
                  ua=None,
                  lang='zh-CN',
                  page_load_strategy='normal',
                  maximize=True):
    """

    :param exe_path:            driver路径
    :param device_name:         模拟H5的设备名称
    :param headless:            无头模式
    :param ua:                  user-agent
    :param lang:                浏览器语言，zh-CN | en-US | km-KH
    :param page_load_strategy:  页面加载策略，none | eager | normal
    :param maximize:            是否最大化窗口

    :return: WebDriver
    """
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.set_capability('noRetest', True)

    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')  # 禁止显示“Chrome正在被自动化软件控制”的通知
    options.add_argument('--disable-notifications')  # 禁用通知
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
    options.add_argument('--no-sandbox')  # bypass OS security model
    options.add_argument('--version')  # 打印chrome浏览器版本
    options.add_argument(f'--lang={lang}')
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    })

    if ua:
        options.add_argument(f'--user-agent={ua}')
    if headless:
        options.add_argument("--window-size=1920,1080")
    if maximize:
        options.add_argument('--start-maximized')  # 最大化模式打开浏览器
    if device_name:
        options.add_experimental_option('mobileEmulation', {'deviceName': device_name})

    caps = webdriver.DesiredCapabilities.CHROME.copy().update({
        'pageLoadStrategy': page_load_strategy
    })

    executable_path = driver_path or chromedriver_last_version_path()

    if headless:
        log.info('无头模式启动chrome driver')
    else:
        log.info('正常模式启动chrome driver')
    log.info(f'chromedriver executable:[ {executable_path} ]')

    wd = webdriver.Chrome(executable_path=executable_path,
                          service_log_path=chromedriver_log_path(),
                          options=options,
                          desired_capabilities=caps)

    atexit.register(wd.quit)  # always quit driver when done
    return wd


def webview_driver(serial,
                   package,
                   activity,
                   process,
                   page_load_strategy='normal',
                   attach=True,
                   driver_path=None):

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # open Browser in maximized mode
    options.add_argument('--no-sandbox')  # bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
    options.add_argument('--disable-extensions')
    options.add_experimental_option('w3c', False)
    options.add_experimental_option('androidDeviceSerial', serial)
    options.add_experimental_option('androidPackage', package)
    options.add_experimental_option('androidActivity', activity)
    options.add_experimental_option('androidUseRunningApp', attach)

    caps = webdriver.DesiredCapabilities.ANDROID.copy().update({
        'pageLoadStrategy': page_load_strategy,
        'unicodeKeyboard': True,  # 使用Unicode编码方式发送字符串
        'resetKeyboard': True  # 隐藏键盘，这样才能输入中文
    })

    executable_path = driver_path or chromedriver_last_version_path()

    log.info('启动chrome driver')
    log.info(f'chromedriver executable:[ {executable_path} ]')
    log.info(f'android serial:[ {serial} ]')
    log.info(f'android package:[ {package} ]')
    log.info(f'android activity:[ {activity} ]')

    wd = webdriver.Chrome(executable_path=executable_path,
                          service_log_path=chromedriver_log_path(),
                          options=options,
                          desired_capabilities=caps)

    atexit.register(wd.quit)  # always quit driver when done
    return wd
