#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : msedgedriver.py
# @Time    : 2020/10/15 23:18
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from clickx3.se.support.driver_util import msedgedriver_last_version_path
from clickx3.se.support.driver_util import msedgedriver_log_path
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)

KEY = 'ms:edgeOptions'


def chrome_to_edge_options(chrome_options):
    caps = chrome_options.to_capabilities()
    caps[KEY] = chrome_options.pop(chrome_options.KEY)
    return caps


def edge_driver(driver_path=None, device_name=None, headless=False, ua=None, lang=None, maximize=True):
    """

    :param exe_path:            driver路径
    :param device_name:         模拟H5的设备名称
    :param headless:            无头模式
    :param ua:                  user-agent
    :param lang:                浏览器语言，zh-CN | en-US | km-KH
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

    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    })

    if ua:
        options.add_argument(f'--user-agent={ua}')
    if lang:
        options.add_argument(f'--lang={lang}')
    if headless:
        options.add_argument("--window-size=1920,1080")
    if maximize:
        options.add_argument('--start-maximized')  # 最大化模式打开浏览器
    if device_name:
        options.add_experimental_option('mobileEmulation', {'deviceName': device_name})

    caps = webdriver.DesiredCapabilities.EDGE.copy()
    caps['pageLoadStrategy'] = 'normal'
    caps.update(chrome_to_edge_options(options))

    executable_path = driver_path or msedgedriver_last_version_path()

    if headless:
        log.info('无头模式启动edge driver')
    else:
        log.info('正常模式启动edge driver')
    log.info(f'msedgedriver executable:[ {executable_path} ]')

    wd = webdriver.Edge(
        executable_path=executable_path,
        service_log_path=msedgedriver_log_path(),
        options=options,
        desired_capabilities=caps
    )

    atexit.register(wd.quit)  # always quit driver when done
    return wd
