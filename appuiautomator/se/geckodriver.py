#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : geckodriver.py
# @Time    : 2020/9/11 15:32
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from appuiautomator.se.driver_util import gecodriver_last_version_path, gecodriver_log_path
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


GECODRIVER_LAST_VERSION_PATH = gecodriver_last_version_path()
GECODRIVER_LOG_PATH = gecodriver_log_path()


IPHONE_X_UA = (
    r'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
    r'Version/12.0 Mobile/15A372 Safari/604.1'
)


def firefox_driver(exe_path=None,
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
    options = webdriver.FirefoxOptions()
    options.headless = headless
    options.set_preference('intl.accept_languages', lang)
    if ua:
        options.set_preference('general.useragent.override', ua)

    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy().update({
        'pageLoadStrategy': page_load_strategy
    })

    executable_path = exe_path or GECODRIVER_LAST_VERSION_PATH

    if headless:
        log.info('无头模式启动firefox driver')
    else:
        log.info('启动firefox driver')
    log.info(f'driver executable path:[ {executable_path} ]')

    wd = webdriver.Firefox(executable_path=executable_path,
                           service_log_path=GECODRIVER_LOG_PATH,
                           options=options,
                           desired_capabilities=desired_capabilities)

    if maximize:
        log.info('最大化窗口')
        wd.maximize_window()

    atexit.register(wd.quit)  # always quit driver when done
    return wd
