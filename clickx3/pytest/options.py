#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : options.py
# @Time    : 2021/5/1 13:39
# @Author  : Kelvin.Ye
import pytest


def pytest_addoption(parser):
    """添加pytest命令行参数"""
    parser.addoption(
        "--env", action="store", default="uat", help="测试环境名称"
    )
    parser.addoption(
        "--headless", action="store", default="true", help="无头模式"
    )


@pytest.fixture(scope='session', autouse=True)
def env(request):
    """环境变量名称"""
    return request.config.getoption("--env")


@pytest.fixture(scope='session', autouse=True)
def headless(request):
    """无头模式"""
    headless = request.config.getoption("--headless")
    return True if headless.lower() == 'true' else False
