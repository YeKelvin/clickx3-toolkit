#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : driver_util.py
# @Time    : 2020/9/11 16:02
# @Author  : Kelvin.Ye
import os
import platform

from clickx3.utils.config import resources_path


def executable_driver_name(driver_name):
    """根据当前操作系统获取驱动名称，Windows的驱动有.exe的后缀"""
    if platform.system() != 'Windows':
        return driver_name
    return driver_name + '.exe'


def last_version(driver_name):
    """根据driver名称获取resources/webdrive/目录下最新版本driver的绝对路径

    Args:
        driver_name (str): chrome | firefox

    Returns:
        None | str
    """
    driver_dir = os.path.join(resources_path(), 'webdrive', driver_name)
    if not os.path.exists(driver_dir):
        raise FileExistsError(f'驱动目录不存在，路径:[ {driver_dir} ]')
    verisons = [ver for ver in os.listdir(driver_dir) if os.path.isdir(os.path.join(driver_dir, ver))]
    verisons.sort()
    return os.path.join(driver_dir, verisons[-1])


def get_version(driver_name, version):
    """根据driver名称和版本号获取driver所在目录的绝对路径"""
    driver_dir = os.path.join(resources_path(), 'webdrive', driver_name, version)
    if not os.path.exists(driver_dir):
        raise FileExistsError(f'驱动版本目录不存在，路径:[ {driver_dir} ]')
    return driver_dir


def get_chromedriver_path(version):
    """根据版本号获取chromedriver的绝对路径"""
    return os.path.join(get_version('chrome', version), executable_driver_name('chromedriver'))


def chromedriver_last_version_path():
    """获取resources/webdrive/chrome目录下版本号最新driver的绝对路径"""
    return os.path.join(last_version('chrome'), executable_driver_name('chromedriver'))


def chromedriver_log_path():
    """获取chromedriver.log的绝对路径"""
    log_dir = os.path.join(resources_path(), 'webdrive', 'chrome')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, 'chromedriver.log')


def gecodriver_last_version_path():
    """获取resources/webdrive/firefox目录下版本号最新driver的绝对路径"""
    return os.path.join(last_version('firefox'), executable_driver_name('geckodriver'))


def gecodriver_log_path():
    """获取geckodriver.log的绝对路径"""
    log_dir = os.path.join(resources_path(), 'webdrive', 'firefox')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, 'geckodriver.log')


def msedgedriver_last_version_path():
    """获取resources/webdrive/edge目录下版本号最新driver的绝对路径"""
    return os.path.join(last_version('edge'), executable_driver_name('msedgedriver'))


def msedgedriver_log_path():
    """获取msedgedriver.log的绝对路径"""
    log_dir = os.path.join(resources_path(), 'webdrive', 'edge')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, 'msedgedriver.log')
