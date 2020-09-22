#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest.py
# @Time    : 2020/9/16 16:09
# @Author  : Kelvin.Ye
import pytest

from appuiautomator.devices_manager import DevicesManager
from appuiautomator.u2 import device
from appuiautomator.u2.device import Device
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)

# 声明排除测试目录或模块
# collect_ignore = ['ignore.py']
# collect_ignore_glob = ['*_ignore.py']

__device__ = None


@pytest.fixture(scope='session')
def an_serial():
    return DevicesManager.android().get_device()


@pytest.fixture(scope='session')
def an_device(an_serial):
    global __device__
    if __device__:
        return __device__
    else:
        __device__ = Device(device.connect(an_serial))


@pytest.fixture(scope='session')
def ios_serial():
    ...


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.get_plugin('html')
    if pytest_html:
        outcome = yield
        result = outcome.get_result()
        extra = getattr(result, 'extra', [])
        # if result.when == 'call' and result.failed:  # 测试执行阶段且测试失败时执行以下动作
        if result.when == 'call':  # 测试执行阶段且测试失败时执行以下动作
            # pytest-html添加截图
            image_name = result.nodeid.replace('::', '_') + '.png'
            extra.append(pytest_html.extras.png(image_name))
            result.extra = extra


def android_screenshot(image_name):
    if __device__:
        __device__.screenshot(image_name)
