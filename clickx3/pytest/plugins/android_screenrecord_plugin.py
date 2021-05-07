#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : android_screenrecord_plugin.py
# @Time    : 2021/5/6 17:14
# @Author  : Kelvin.Ye
import os

from clickx3.pytest.utils import node_id_to_name
from clickx3.utils import project
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


def pytest_runtest_setup(item):
    """测试失败重跑时，开始录屏"""
    execution_count = getattr(item, 'execution_count', 1)
    if execution_count > 1:
        # 没有使用安卓设备时无需录屏
        device = item.funcargs.get('android_device')
        if not device:
            return

        # 开始录屏
        video_name = node_id_to_name(item.nodeid)
        start_android_screenrecord(device, video_name)


def pytest_runtest_makereport(item, result):
    """测试失败重跑后还是失败时添加录屏"""
    if not (result.when == 'call'):
        return

    # 测试失败重跑后还是失败时，添加录屏
    execution_count = getattr(item, 'execution_count', 1)
    if execution_count > 1:
        # 没有使用安卓设备时无需录屏
        device = item.funcargs.get('android_device')
        if not device:
            return

        # 停止录屏
        video_name = node_id_to_name(item.nodeid)
        video_path = stop_android_screenrecord(device, video_name)

        # 没有使用pytest-html插件时无需录屏
        pytest_html = item.config.pluginmanager.get_plugin('html')
        if not pytest_html:
            return

        if result.failed:
            extra = getattr(result, 'extra', [])
            extra.append(pytest_html.extras.mp4(video_path))
            result.extra = extra


def start_android_screenrecord(device, video_name):
    log.info('Android开始录屏')
    video_path = os.path.join(project.screenrecord_path(), f'{video_name}.android.mp4')
    device.screenrecord(video_path)


def stop_android_screenrecord(device, video_name):
    if not device.screenrecord._running:
        return

    log.info('Android停止录屏')
    device.screenrecord.stop()
    video_path = os.path.join(project.screenrecord_path(), f'{video_name}.android.mp4')
    log.info(f'录屏文件路径:[ {video_path} ]')
    return video_path
