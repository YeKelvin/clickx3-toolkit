#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pytest_demo.py
# @Time    : 2019/9/18 19:15
# @Author  : Kelvin.Ye
import os

import allure
import pytest


def setup_function():
    print('setup_function():每个函数之前执行')


def teardown_function():
    print('teardown_function():每个函数之后执行')


def setup_module():
    print('setup_module():每个模块运行前执行')


def teardown_module():
    print('teardown_module():每个模块运行后执行')


@pytest.fixture(params=[{'keyA': 'valueA'}, {'keyB': 'valueB'}])
def data(params):
    return params.param


def test_fixture(data):
    print(data)


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


@allure.feature('标注功能or模块')
class TestAllureDemo:
    @allure.story("标注子功能or模块")
    def test_story(self):
        pass

    @allure.severity('标注案例重要程度')
    def test_severity(self):
        pass

    @allure.step('标注案例步骤')
    def test_step(self):
        pass

    def test_step2(self):
        with allure.step('步骤1'):
            a = 1
        with allure.step('步骤2'):
            b = 1
        assert a == b

    def test_attach_info(self):
        allure.attach('附加信息')

    def test_attach_picture(self):
        with open(r'filepath.jpg', 'rb') as file:
            allure.attach(file.read(), name='附加图片', attachment_type=allure.attachment_type.JPG)

    @allure.testcase('案例链接', '链接名称')
    def test_testcase(self):
        pass

    @allure.issue('问题链接', '链接名称')
    def test_issue(self):
        pass

    @allure.description('案例描述')
    def test_description(self):
        pass


if __name__ == '__main__':
    """python代码中运行pytest
    """
    pytest.main(['-s', f'{os.path.basename(__file__)}::test_parametrize'])
    pytest.main(['-s', f'{os.path.basename(__file__)}', '--html=./report.html'])
    pytest.main(['-s', f'{os.path.basename(__file__)}', '--alluredir=./report', '--clean-alluredir'])

"""
生成 Allure HTML报告

下载 allure-command，下载地址: https://github.com/allure-framework/allure2/releases
解压后，PATH环境变量添加 allure/bin路径

allure generate report -o html --clean
"""
