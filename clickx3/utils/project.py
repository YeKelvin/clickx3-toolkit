#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : project.py
# @Time    : 2021/5/2 19:04
# @Author  : Kelvin.Ye
from functools import lru_cache
import os

from clickx3.utils.ini_reader import IniConfig
from clickx3.utils.path_util import find_invoker_project_root

# 项目名称
name = None


@lru_cache
def root_path():
    """项目根目录路径"""
    return find_invoker_project_root(name)


@lru_cache
def config_path():
    """配置文件路径"""
    return os.path.join(root_path(), 'config.ini')


config = IniConfig(config_path())


@lru_cache
def resources_path():
    """项目资源目录路径"""
    resources = os.path.normpath(config.get('path', 'resources'))
    return os.path.join(root_path(), resources)


@lru_cache
def environment_path():
    """环境配置文件目录路径"""
    resources = os.path.normpath(config.get('path', 'environment'))
    return os.path.join(root_path(), resources)


@lru_cache
def screenrecord_path():
    """录屏视频目录路径"""
    screenrecord = os.path.normpath(config.get('path', 'screenrecord'))
    return os.path.join(root_path(), screenrecord)


@lru_cache
def screenshot_path():
    """截图目录路径"""
    screenshot = os.path.normpath(config.get('path', 'screenshot'))
    return os.path.join(root_path(), screenshot)


@lru_cache
def default_image_path():
    """默认图片路径"""
    default_image = os.path.normpath(config.get('path', 'default_image'))
    return os.path.join(root_path(), default_image)
