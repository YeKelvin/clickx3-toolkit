#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : driver_util.py
# @Time    : 2020/9/11 16:02
# @Author  : Kelvin.Ye
import os

from appuiautomator.utils.config import resources_path


def last_version_dir(driver_name):
    driver_dir = os.path.join(resources_path(), 'webdrive', driver_name)
    verisons = os.listdir(driver_dir)
    verisons.sort()
    return os.path.join(driver_dir, verisons[-1])


def chromedriver_last_version_path():
    return os.path.join(last_version_dir('chrome'), 'chromedriver.exe')


def chromedriver_log_path():
    return os.path.join(last_version_dir('chrome'), 'chromedriver.log')


def gecodriver_last_version_path():
    return os.path.join(last_version_dir('firefox'), 'geckodriver.exe')


def gecodriver_log_path():
    return os.path.join(last_version_dir('firefox'), 'geckodriver.log')
