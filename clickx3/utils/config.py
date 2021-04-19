#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2019/8/27 12:01
# @Author  : Kelvin.Ye
import configparser
import os

__CONFIG_PATH__ = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'config.ini'))


def get(section, key, filepath=__CONFIG_PATH__):
    """获取配置文件中的属性值，默认读取config.ini。

    Args:
        section: section名
        key: 属性名
        filepath: 配置文件路径

    Returns:
        属性值
    """
    if not os.path.exists(filepath):
        raise FileExistsError(filepath + ' 配置文件不存在')
    config = configparser.ConfigParser()
    config.read(filepath)
    return config.get(section, key)


def project_path():
    """返回项目根目录路径。
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def resources_path():
    """返回项目资源目录路径。
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'resources'))


def screenrecord_path():
    """返回录屏视频目录路径
    """
    return os.path.join(project_path(), 'testcases', '.screenrecords')


def screenshot_path():
    """返回截图目录路径
    """
    return os.path.join(project_path(), 'testcases', '.screenshots')


def default_test_image_path():
    return os.path.join(resources_path(), 'testimage', 'default.png')


if __name__ == '__main__':
    print(__CONFIG_PATH__)
    print(project_path())
    print(resources_path())
