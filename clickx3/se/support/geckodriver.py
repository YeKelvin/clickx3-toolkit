#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : geckodriver.py
# @Time    : 2020/9/11 15:32
# @Author  : Kelvin.Ye
import atexit

from selenium import webdriver

from clickx3.se.support.driver_util import gecodriver_last_version_path
from clickx3.se.support.driver_util import gecodriver_log_path
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)

IPHONE_X_UA = (
    r'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
    r'Version/12.0 Mobile/15A372 Safari/604.1'
)


def firefox_driver(exe_path=None, headless=False, ua=None, lang=None, maximize=True):
    """

    :param exe_path:            driver路径
    :param log_path:            driver日志路径
    :param headless:            无头模式
    :param ua:                  user-agent
    :param maximize:            是否最大化窗口

    :return: WebDriver
    """
    options = webdriver.FirefoxOptions()
    options.headless = headless
    options.add_argument('-safe-mode')  # 不加载任何扩展(Extensions)、主题(Theme)和插件(Plugins)
    options.set_preference('devtools.debugger.remote-enabled', True)
    options.set_preference('devtools.debugger.prompt-connection', False)
    options.set_preference('devtools.chrome.enabled', True)
    options.set_preference('browser.fullscreen.autohide', True)  # 在全屏模式下隐藏工具栏
    options.set_preference('geo.enabled', True)  # 地理位置
    options.set_preference('signon.showAutoCompleteFooter', True)  # 在登录表单中查看密码

    if ua:
        options.set_preference('general.useragent.override', ua)
    if lang:
        options.set_preference('intl.accept_languages', lang)
    if headless:
        options.add_argument("--window-size=1920,1080")

    caps = webdriver.DesiredCapabilities.FIREFOX.copy()
    caps['pageLoadStrategy'] = 'normal'

    executable_path = exe_path or gecodriver_last_version_path()

    if headless:
        log.info('无头模式启动firefox driver')
    else:
        log.info('正常模式启动firefox driver')
    log.info(f'geckodriver executable:[ {executable_path} ]')

    wd = webdriver.Firefox(
        executable_path=executable_path,
        service_log_path=gecodriver_log_path(),
        options=options,
        desired_capabilities=caps
    )

    if maximize:
        log.info('最大化窗口')
        wd.maximize_window()

    atexit.register(wd.quit)  # always quit driver when done
    return wd


def gecko_view(serial, package, activity, driver_path=None):
    """
    {
        "capabilities": {
            "alwaysMatch": {
            "moz:firefoxOptions": {
                "androidPackage": "org.mozilla.geckoview_example",
                "androidActivity": "org.mozilla.geckoview_example.GeckoView",
                "androidDeviceSerial": "emulator-5554",
                "androidIntentArguments": [
                "-d", "http://example.org"
                ],
                "env": {
                "MOZ_LOG": "nsHttp:5",
                "MOZ_LOG_FILE": "/mnt/sdcard/log"
                }
            }
            }
        }
    }
    """
    options = webdriver.FirefoxOptions()
    options.set_capability('w3c', False)
    options.set_capability('androidDeviceSerial', serial)
    options.set_capability('androidPackage', package)
    options.set_capability('androidActivity', activity)
    options.set_capability('androidUseRunningApp', True)

    caps = webdriver.DesiredCapabilities.ANDROID.copy().update({
        'pageLoadStrategy': 'normal',
        'unicodeKeyboard': True,  # 使用Unicode编码方式发送字符串
        'resetKeyboard': True  # 隐藏键盘，这样才能输入中文
    })

    executable_path = driver_path or gecodriver_last_version_path()

    log.info('启动chrome driver')
    log.info(f'chromedriver executable:[ {executable_path} ]')
    log.info(f'android serial:[ {serial} ]')
    log.info(f'android package:[ {package} ]')
    log.info(f'android activity:[ {activity} ]')

    wd = webdriver.Firefox(
        executable_path=executable_path,
        service_log_path=gecodriver_log_path(),
        options=options,
        desired_capabilities=caps
    )

    atexit.register(wd.quit)  # always quit driver when done
    return wd
