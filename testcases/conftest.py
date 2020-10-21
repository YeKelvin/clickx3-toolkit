#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest.py
# @Time    : 2020/9/16 16:09
# @Author  : Kelvin.Ye
import os

import pytest
# from py._xmlgen import html

from appuiautomator.devices_manager import DevicesManager
from appuiautomator.u2 import device
from appuiautomator.u2.device import Device
from appuiautomator.utils.config import screenrecord_path, screenshot_path
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


# def pytest_html_report_title(report):
#     report.title = 'APP UI自动化测试报告'


# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('Description'))


# def pytest_html_results_table_row(report, cells):
#     cells.insert(1, html.td(report.description))


def pytest_runtest_call(item):
    execution_count = getattr(item, 'execution_count', 1)
    if execution_count > 1:  # 测试用例重跑时，开始录屏
        an_device = item.funcargs.get('an_device')
        if an_device:
            video_name = item.nodeid.replace('::', '_')
            video_path = _android_screenshot(an_device, video_name)
            _android_start_screenrecord(an_device, video_path)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    result.description = str(item.function.__doc__)  # 添加测试用例描述

    if result.when == 'call':
        pytest_html = item.config.pluginmanager.get_plugin('html')
        an_device = item.funcargs.get('an_device')
        if pytest_html and an_device:
            _actions_after_failed_test(item, result, pytest_html, an_device)


def _actions_after_failed_test(item, result, pytest_html, an_device):
    execution_count = getattr(item, 'execution_count', 1)
    extra = getattr(result, 'extra', [])
    nodeid = item.nodeid.replace('::', '_')
    if execution_count == 1:  # 测试用例首次失败时，pytest-html添加截图
        if result.failed:
            image_path = _android_screenshot(an_device, nodeid)
            extra.append(pytest_html.extras.png(image_path))
            result.extra = extra
    elif execution_count > 1:  # 测试用例重跑时，pytest-html添加录屏视频
        video_path = _android_stop_screenrecord(an_device, nodeid)
        if result.failed:
            extra.append(pytest_html.extras.mp4(video_path))
            result.extra = extra


def _android_screenshot(an_device, image_name):
    log.info('开始截图')
    image_path = os.path.join(screenshot_path(), f'{image_name}.png')
    an_device.screenshot(image_path)
    log.info(f'截图保存路径={image_path}')
    return image_path


def _android_start_screenrecord(an_device, video_name):
    log.info('开始录屏')
    video_path = os.path.join(screenrecord_path(), f'{video_name}.mp4')
    an_device.screenrecord(video_path)


def _android_stop_screenrecord(an_device, video_name):
    log.info('停止录屏')
    an_device.screenrecord.stop()
    video_path = os.path.join(screenrecord_path(), f'{video_name}.mp4')
    log.info(f'视频保存路径={video_path}')
    return video_path
