#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest.py
# @Time    : 2020/9/16 16:09
# @Author  : Kelvin.Ye
import os

import pytest
from clickx3.common.devices_manager import DevicesManager
from clickx3.se.driver import Driver
from clickx3.u2.device import Device
from clickx3.utils.config import screenrecord_path, screenshot_path
from clickx3.utils.log_util import get_logger

# from py._xmlgen import html


log = get_logger(__name__)


# 声明排除测试目录或模块
# collect_ignore = ['ignore.py']
# collect_ignore_glob = ['*_ignore.py']


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="uat", help="测试环境名称"
    )
    parser.addoption(
        "--headless", action="store", default="true", help="无头模式"
    )


@pytest.fixture(autouse=True)
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(autouse=True)
def headless(request):
    return bool(request.config.getoption("--headless"))


@pytest.fixture(autouse=True)
def ctx(request):
    return request


@pytest.fixture(scope='session', autouse=True)
def props():
    return {}


@pytest.fixture(scope='class', autouse=True)
def vars():
    return {}


@pytest.fixture(scope='session')
def web_driver():
    # driver = Driver.chrome()
    driver = Driver.chrome(headless=True)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='session')
def chrome_driver(headless):
    driver = Driver.chrome(headless=headless)
    return driver


@pytest.fixture(scope='session')
def firefox_driver(headless):
    driver = Driver.firefox(headless=headless)
    return driver


@pytest.fixture(scope='session')
def edge_driver(headless):
    driver = Driver.edge()(headless=headless)
    return driver


@pytest.fixture(scope='session')
def android_serial():
    return DevicesManager.android().get_device()


@pytest.fixture(scope='session')
def android_device(android_serial):
    return Device.connect(android_serial)


@pytest.fixture(scope='session')
def chrome_webview(android_device):
    from pages.chrome.android import Chrome
    return Chrome(android_device).webview


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
        if android_device:
            video_name = __get_node_name(item.nodeid)
            __android_start_screenrecord(item, video_name)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    result.description = str(item.function.__doc__)  # 添加测试用例描述

    if result.when == 'call':
        pytest_html = item.config.pluginmanager.get_plugin('html')
        if pytest_html:
            __actions_after_failed_test(item, result, pytest_html)


def __actions_after_failed_test(item, result, pytest_html):
    execution_count = getattr(item, 'execution_count', 1)
    extra = getattr(result, 'extra', [])
    media_name = __get_node_name(item.nodeid)
    if execution_count == 1:  # 测试用例首次失败时，pytest-html添加截图
        if result.failed:
            __android_screenshot(item, media_name, extra, pytest_html)
            __web_screenshot(item, media_name, extra, pytest_html)
            result.extra = extra
    elif execution_count > 1:  # 测试用例重跑时，pytest-html添加录屏视频
        video_path = __android_stop_screenrecord(item, media_name)
        if result.failed:
            extra.append(pytest_html.extras.mp4(video_path))
            result.extra = extra


def __get_node_name(nodeid):
    formatted_nodeid = nodeid.replace('.py', '').replace('::', '.')
    if os.sep in formatted_nodeid:
        return formatted_nodeid.split(os.sep)[-1]
    else:
        return formatted_nodeid.split('/')[-1]


def __android_screenshot(item, image_name, extra, pytest_html):
    android_device = item.funcargs.get('android_device')
    if android_device:
        log.info('Android截图')
        image_path = os.path.join(screenshot_path(), f'{image_name}.android.png')
        log.info(f'截图保存路径={image_path}')
        android_device.screenshot(image_path)
        extra.append(pytest_html.extras.png(image_path))


def __web_screenshot(item, image_name, extra, pytest_html):
    web_driver = item.funcargs.get('web_driver')
    if web_driver:
        log.info('Web截图')
        image_path = os.path.join(screenshot_path(), f'{image_name}.web.png')
        log.info(f'截图保存路径={image_path}')
        web_driver.save_screenshot(image_path)
        extra.append(pytest_html.extras.png(image_path))


def __android_start_screenrecord(item, video_name):
    android_device = item.funcargs.get('android_device')
    if android_device:
        log.info('开始录屏')
        video_path = os.path.join(screenrecord_path(), f'{video_name}.mp4')
        android_device.screenrecord(video_path)


def __android_stop_screenrecord(item, video_name):
    android_device = item.funcargs.get('android_device')
    if android_device and android_device.screenrecord._running:
        log.info('停止录屏')
        android_device.screenrecord.stop()
        video_path = os.path.join(screenrecord_path(), f'{video_name}.mp4')
        log.info(f'视频保存路径={video_path}')
        return video_path
