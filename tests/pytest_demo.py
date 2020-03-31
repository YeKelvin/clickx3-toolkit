#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pytest_demo.py
# @Time    : 2019/9/18 19:15
# @Author  : Kelvin.Ye
import os

import pytest


def setup_function():
    print('setup_function():每个函数之前执行')


def teardown_function():
    print('teardown_function():每个函数之后执行')


def setup_module():
    print('setup_module():每个模块运行前执行')


def teardown_module():
    print('teardown_module():每个模块运行后执行')


class TestMethod:
    def setup_class(self):
        print('setup_class(self)：每个类之前执行一次')

    def teardown_class(self):
        print('teardown_class(self)：每个类之后执行一次')

    def setup_method(self):
        print('setup_method(self):在每个类或实例方法之前执行')

    def teardown_method(self):
        print('teardown_method(self):在每个类或实例方法之后执行')

    def test_method(self):
        print('method')


@pytest.mark.parametrize('key_name', ['key_value'])
def test_parametrize(key_name):
    """参数化
    """
    print(key_name)


if __name__ == '__main__':
    """python代码中运行pytest
    """
    pytest.main(['-s', f'{os.path.basename(__file__)}::test_parametrize'])
    pytest.main(['-s', f'{os.path.basename(__file__)}', '--html=report.html'])
