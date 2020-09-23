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


@pytest.fixture(scope='session')
def an_serial():
    return DevicesManager.android().get_device()


@pytest.fixture(scope='session')
def an_device(an_serial):
    return Device(device.connect(an_serial))


@pytest.fixture(scope='session')
def ios_serial():
    ...


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    pytest_html = item.config.pluginmanager.get_plugin('html')
    an_device = item.funcargs.get('an_device')
    if pytest_html and an_device:
        result = outcome.get_result()
        if result.when == 'call' and result.failed:  # 测试执行阶段且测试失败时执行以下动作
            actions_after_failed_test(item, result, pytest_html, an_device)


def actions_after_failed_test(item, result, pytest_html, an_device):
    execution_count = getattr(item, 'execution_count', 1)
    extra = getattr(result, 'extra', [])
    nodeid = item.nodeid.replace('::', '_')
    if execution_count == 1:  # pytest-html添加截图
        image_path = _android_screenshot(an_device, nodeid)
        extra.append(pytest_html.extras.png(image_path))
        result.extra = extra
    elif execution_count > 1:  # pytest-html添加录屏
        video_path = _android_stop_screenrecord(an_device, nodeid)
        extra.append(pytest_html.extras.mp4(video_path))
        result.extra = extra


# def pytest_runtest_call(item):
#     execution_count = getattr(item, 'execution_count', 1)
#     if execution_count > 1:
#         an_device = item.funcargs.get('an_device')
#         if an_device:
#             video_name = item.nodeid.replace('::', '_')
#             video_path = _android_screenshot(an_device, video_name)
#             _android_start_screenrecord(an_device, video_path)


def _android_screenshot(an_device, image_name):
    log.info('开始截图')
    image_path = f'./.screenshots/{image_name}.png'
    an_device.screenshot(image_path)
    log.info(f'截图保存路径={image_path}')
    return image_path


def _android_start_screenrecord(an_device, video_name):
    log.info('开始录屏')
    video_path = f'./.screenrecords/{video_name}.mp4'
    an_device.screenrecord(video_path)


def _android_stop_screenrecord(an_device, video_name):
    log.info('结束录屏')
    an_device.screenrecord.stop()
    video_path = f'./.screenrecords/{video_name}.mp4'
    log.info(f'视频保存路径={video_path}')
    return video_path
