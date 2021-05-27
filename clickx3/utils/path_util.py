#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : path_util.py
# @Time    : 2021/5/2 14:17
# @Author  : Kelvin.Ye
import os
import sys

from clickx3.common.exceptions import ProjectBaseDirectoryNotFoundException


# 项目构建文件列表
__CONFIG_FILE_LIST__ = ['pyproject.toml', 'tox.ini', 'setup.cfg', 'setup.py']


def find_invoker_project_root(name=None, target='pyproject.toml'):
    """查找项目根路径"""
    if name:
        return __find_project_root_by_name(name)
    else:
        return __find_project_root_by_target(target)


def __find_project_root_by_name(name):
    """根据项目名称查找项目根路径"""
    # 尝试在执行路径上查找
    cwd_dir = os.getcwd()
    if cwd_dir and (name in cwd_dir):
        start_index = cwd_dir.find(name)
        if start_index > 0:
            return cwd_dir[:start_index + len(name)]

    # 尝试在调用文件路径上查找
    invoker_dir = sys.path[0]
    if invoker_dir and (name in invoker_dir):
        start_index = invoker_dir.find(name)
        if start_index > 0:
            return invoker_dir[:start_index + len(name)]

    raise ProjectBaseDirectoryNotFoundException(
        f'查找项目根路径失败，尝试查找的路径\n'
        f'name:[ {name} ]\n'
        f'cwd:[ {cwd_dir} ]\n'
        f'invoker:[ {invoker_dir} ]'
    )


def __find_project_root_by_target(target):
    """根据目标文件名称查找项目根路径"""
    cwd_parent_dir = os.getcwd()
    previous_cwd_dir = ''
    while True:
        if previous_cwd_dir == cwd_parent_dir:
            break
        if __has_target(cwd_parent_dir, target):
            return cwd_parent_dir
        previous_cwd_dir = cwd_parent_dir
        invoker_parent_dir = __get_pardir(cwd_parent_dir)

    invoker_parent_dir = sys.path[0]
    previous_invoker_dir = ''
    while True:
        if previous_invoker_dir == invoker_parent_dir:
            break
        if __has_target(invoker_parent_dir, target):
            return invoker_parent_dir
        previous_invoker_dir = invoker_parent_dir
        invoker_parent_dir = __get_pardir(invoker_parent_dir)

    raise ProjectBaseDirectoryNotFoundException(
        f'查找项目根路径失败，尝试查找的路径\n'
        f'target:[ {target} ]\n'
        f'cwd:[ {cwd_parent_dir} ]\n'
        f'invoker:[ {invoker_parent_dir} ]'
    )


def __has_target_by_str(parent_directory, target):
    target_path = os.path.join(parent_directory, target)
    return os.path.isfile(target_path)


def __has_target_by_list(parent_directory, targets):
    for target in targets:
        target_path = os.path.join(parent_directory, target)
        if os.path.isfile(target_path):
            return True

    return False


def __has_target(parent_directory, target) -> bool:
    """判断目录里是否包含目标文件"""
    if not parent_directory:
        return False

    if isinstance(target, list):
        return __has_target_by_list(parent_directory, target)

    if isinstance(target, str):
        return __has_target_by_str(parent_directory, target)

    return False


def __get_pardir(dir):
    return os.path.abspath(os.path.join(dir, os.pardir))
