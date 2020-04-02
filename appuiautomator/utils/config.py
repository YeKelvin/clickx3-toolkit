#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2019/8/27 12:01
# @Author  : Kelvin.Ye
import os
import configparser

_CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'config.ini')
)


def get(section, key, filepath=_CONFIG_PATH):
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


def get_project_path():
    """返回项目根目录路径。
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def get_screenshot_path():
    """返回截图目录路径
    """
    return os.path.join(get_project_path(), 'testcases', '.tmp')


if __name__ == '__main__':
    print(_CONFIG_PATH)
    print(get_project_path())
