#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : driver_util
# @Time    : 2020/9/11 16:02
# @Author  : Kelvin.Ye
import os

from appuiautomator.utils.config import resources_path


def last_version_dir(driver_name):
    driver_dir = os.path.join(resources_path(), 'webdrive', driver_name)
    verisons = os.listdir(driver_dir)
    verisons.sort()
    return os.path.join(driver_dir, verisons[-1])


def last_chromedriver_path():
    return os.path.join(last_version_dir('chrome'), 'chromedriver.exe')


def last_gecodriver_path():
    return os.path.join(last_version_dir('firefox'), 'geckodriver.exe')
