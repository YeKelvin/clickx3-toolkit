#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : web_screenrecord_plugin.py
# @Time    : 2021/5/8 10:00
# @Author  : Kelvin.Ye
import os

from clickx3.pytest.utils import node_id_to_name
from clickx3.utils import project
from clickx3.utils.log_util import get_logger


log = get_logger(__name__)


def pytest_runtest_call(item):
    """失败重跑时，开始录屏"""
    # 没有使用pytest-html插件时无需录屏
    if not item.config.pluginmanager.has_plugin('html'):
        return

    # 失败重跑时开始录屏
    execution_count = getattr(item, 'execution_count', 1)
    if execution_count > 1:

        video_name = node_id_to_name(item.nodeid)

        # Chrome开始录屏
        driver = item.funcargs.get('chrome_driver')
        if driver:
            log.info('Chrome开始录屏')
            start_web_screenrecord(driver, f'{video_name}.chrome')

        # Firefox开始录屏
        driver = item.funcargs.get('firefox_driver')
        if driver:
            log.info('Firefox开始录屏')
            start_web_screenrecord(driver, f'{video_name}.firefox')

        # Edge开始录屏
        driver = item.funcargs.get('edge_driver')
        if driver:
            log.info('Edge开始录屏')
            start_web_screenrecord(driver, f'{video_name}.edge')


def pytest_runtest_makereport(item, result):
    """失败重跑时添加录屏视频"""
    if not (result.when == 'call'):
        return

    # 没有使用pytest-html插件时无需录屏
    pytest_html = item.config.pluginmanager.get_plugin('html')
    if not pytest_html:
        return

    # 测试失败重跑时添加录屏
    execution_count = getattr(item, 'execution_count', 1)
    if execution_count > 1:

        extra = getattr(result, 'extra', [])
        video_name = node_id_to_name(item.nodeid)

        # Chrome停止录屏
        driver = item.funcargs.get('chrome_driver')
        if driver:
            log.info('Chrome停止录屏')
            video_path = stop_web_screenrecord(driver, f'{video_name}.chrome')
            extra.append(pytest_html.extras.mp4(video_path))

        # Firefox停止录屏
        driver = item.funcargs.get('firefox_driver')
        if driver:
            log.info('Firefox停止录屏')
            video_path = stop_web_screenrecord(driver, f'{video_name}.firefox')
            extra.append(pytest_html.extras.mp4(video_path))

        # Edge停止录屏
        driver = item.funcargs.get('edge_driver')
        if driver:
            log.info('Edge停止录屏')
            video_path = stop_web_screenrecord(driver, f'{video_name}.edge')
            extra.append(pytest_html.extras.mp4(video_path))

        result.extra = extra


def start_web_screenrecord(device, video_name):
    video_path = os.path.join(project.screenrecord_path(), f'{video_name}.web.mp4')
    device.screenrecord(video_path)


def stop_web_screenrecord(device, video_name):
    if not device.screenrecord._running:
        return

    device.screenrecord.stop()
    video_path = os.path.join(project.screenrecord_path(), f'{video_name}.web.mp4')
    log.info(f'录屏文件路径:[ {video_path} ]')
    return video_path
