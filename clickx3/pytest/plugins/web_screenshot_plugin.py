#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : web_screenshot_plugin.py
# @Time    : 2021/5/6 17:09
# @Author  : Kelvin.Ye
import os

from clickx3.pytest.utils import node_id_to_name
from clickx3.utils import project
from clickx3.utils.log_util import get_logger


log = get_logger(__name__)


def pytest_runtest_makereport(item, result):
    """首次失败时截图"""
    if not (result.when == 'call'):
        return

    # 没有使用pytest-html插件时无需截图
    pytest_html = item.config.pluginmanager.get_plugin('html')
    if not pytest_html:
        return

    # 测试首次失败时才截图，非首次失败时无需截图
    execution_count = getattr(item, 'execution_count', 1)
    if not (execution_count == 1):
        return

    # 测试通过时无需截图
    if not result.failed:
        return

    extra = getattr(result, 'extra', [])
    image_name = node_id_to_name(item.nodeid)

    # chrome截图
    driver = item.funcargs.get('chrome_driver')
    if driver:
        image_path = web_screenshot(driver, f'{image_name}.chrome')
        extra.append(pytest_html.extras.png(image_path))

    # firefox截图
    driver = item.funcargs.get('firefox_driver')
    if driver:
        image_path = web_screenshot(driver, f'{image_name}.firefox')
        extra.append(pytest_html.extras.png(image_path))

    # edge截图
    driver = item.funcargs.get('edge_driver')
    if driver:
        image_path = web_screenshot(driver, f'{image_name}.edge')
        extra.append(pytest_html.extras.png(image_path))

    result.extra = extra


def web_screenshot(driver, image_name):
    log.info('Web截图')
    image_path = os.path.join(project.screenshot_path(), f'{image_name}.web.png')
    log.info(f'截图文件路径:[ {image_path} ]')
    driver.save_screenshot(image_path)
    return image_path
