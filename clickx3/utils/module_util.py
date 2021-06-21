#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : module_util.py
# @Time    : 2021/6/21 11:14
# @Author  : Kelvin.Ye
import importlib.util


def import_module_by_source(module_name: str, module_path: str):
    """从源文件import模块

    Args:
        module_name (str): 模块名称
        module_path (str): 模块路径

    """
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
