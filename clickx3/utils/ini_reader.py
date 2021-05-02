#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ini_reader.py
# @Time    : 2021/5/2 15:57
# @Author  : Kelvin.Ye
import configparser
import os


def get(section, key, config_path=None):
    """从ini配置文件中获取配置

    Args:
        section: section名
        key: 属性名
        config_path: ini文件路径

    Returns:
        value
    """

    if not os.path.exists(config_path):
        raise FileExistsError(f'ini配置文件不存在，ini path:[ {config_path} ]')

    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get(section, key)


class IniConfig:
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileExistsError(f'ini配置文件不存在，path:[ {path} ]')

        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, section, key):
        return self.config.get(section, key)
