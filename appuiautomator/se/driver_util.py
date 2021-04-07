#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : driver_util.py
# @Time    : 2020/9/11 16:02
# @Author  : Kelvin.Ye
import os

from appuiautomator.utils.config import resources_path


def last_version(driver_name):
    """根据driver-name获取./resources/webdrive/目录下最新版本driver的绝对路径

    Args:
        driver_name (str): chrome | firefox

    Returns:
        None | str
    """
    driver_dir = os.path.join(resources_path(), 'webdrive', driver_name)
    if not os.path.exists(driver_dir):
        return None
    verisons = os.listdir(driver_dir)
    verisons.sort()
    return os.path.join(driver_dir, verisons[-1])


def chromedriver_last_version_path():
    return os.path.join(last_version('chrome'), 'chromedriver.exe')


def chromedriver_log_path():
    log_dir = os.path.join(resources_path(), 'webdrive', 'chrome')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, 'chromedriver.log')


def gecodriver_last_version_path():
    return os.path.join(last_version('firefox'), 'geckodriver.exe')


def gecodriver_log_path():
    log_dir = os.path.join(resources_path(), 'webdrive', 'firefox')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, 'geckodriver.log')
