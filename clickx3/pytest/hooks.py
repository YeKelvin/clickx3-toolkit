#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : hooks.py
# @Time    : 2021/5/6 17:16
# @Author  : Kelvin.Ye
import pytest

from clickx3.pytest.plugins import android_screenrecord_plugin
from clickx3.pytest.plugins import android_screenshot_plugin
from clickx3.pytest.plugins import pytest_html_plugin
from clickx3.pytest.plugins import web_screenrecord_plugin
from clickx3.pytest.plugins import web_screenshot_plugin


def pytest_configure(config):
    # 添加数据
    config._metadata['Project'] = 'UI测试自动化'
    # 删除JAVA_HOME
    config._metadata.pop('JAVA_HOME')


def pytest_runtest_call(item):
    # Android重跑时录屏
    android_screenrecord_plugin.pytest_runtest_call(item)
    # Web重跑时录屏
    web_screenrecord_plugin.pytest_runtest_call(item)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()

    # 优化pytest-html插件
    pytest_html_plugin.pytest_runtest_makereport(item, result)

    # Android失败时截图
    android_screenshot_plugin.pytest_runtest_makereport(item, result)
    # Android失败重跑时添加录屏
    android_screenrecord_plugin.pytest_runtest_makereport(item, result)

    # Web失败时截图
    web_screenshot_plugin.pytest_runtest_makereport(item, result)
    # Web失败重跑时添加录屏
    web_screenrecord_plugin.pytest_runtest_makereport(item, result)
