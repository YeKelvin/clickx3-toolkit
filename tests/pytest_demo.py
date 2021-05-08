#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pytest_demo.py
# @Time    : 2019/9/18 19:15
# @Author  : Kelvin.Ye
import pytest


def setup_module():
    print('setup_module()：模块加载前调用')


def teardown_module():
    print('teardown_module()：模块执行后调用')


def setup_function():
    print('setup_function()：函数执行前调用')


def teardown_function():
    print('teardown_function()：函数执行后调用')


def test_function():
    print('测试函数')


@pytest.fixture
def define_a_fixture():
    return '定义一个fixture'


def test_use_fixture(define_a_fixture):
    print(f'使用fixture参数，fixture={define_a_fixture}')


@pytest.fixture(params=[{'keyA': 'valueA'}, {'keyB': 'valueB'}])
def define_a_params(request):
    """定义测试数据"""
    return request.param


def test_use_params(define_a_params):
    print(f'使用测试数据，params={define_a_params}')


@pytest.mark.parametrize('key', ['value1', 'value2'])
def test_parametrize(key):
    """参数化"""
    print(key)


class ClassTestSuite:

    def setup_class(cls):
        print('setup_class()：类执行前调用，参数只有cls，不能使用fixture')

    def teardown_class(cls):
        print('teardown_class()：类全部执行完后调用，参数只有cls，不能使用fixture')

    def setup_method(self):
        print('setup_method()：方法执行前调用')

    def teardown_method(self):
        print('teardown_method()：方法执行后调用')

    def test_method(self):
        print('测试方法')


# @allure.feature('标注功能or模块')
# class AllureTestSuite:
#     @allure.story("标注子功能or模块")
#     def test_story(self):
#         pass

#     @allure.severity('标注案例重要程度')
#     def test_severity(self):
#         pass

#     @allure.step('标注案例步骤')
#     def test_step(self):
#         pass

#     def test_step2(self):
#         with allure.step('步骤1'):
#             a = 1
#         with allure.step('步骤2'):
#             b = 1
#         assert a == b

#     def test_attach_info(self):
#         allure.attach('附加信息')

#     def test_attach_picture(self):
#         with open(r'baozou.png', 'rb') as file:
#             allure.attach(file.read(), name='附加图片', attachment_type=allure.attachment_type.JPG)

#     @allure.testcase('案例链接', '链接名称')
#     def test_testcase(self):
#         pass

#     @allure.issue('问题链接', '链接名称')
#     def test_issue(self):
#         pass

#     @allure.description('案例描述')
#     def test_description(self):
#         pass


if __name__ == '__main__':
    """python代码中运行pytest
    """
    # import os
    # target = ['-s', '-v', f'{os.path.basename(__file__)}::function_name']
    # target = ['-s', '-v', f'{os.path.basename(__file__)}::class_name::method_name']
    # target = ['-s', '-v', f'{os.path.basename(__file__)}', '--html=./report.html']
    # pytest.main(target)

    # from subprocess import Popen, PIPE
    # p = Popen('allure generate .report -o .html --clean', shell=True, stdout=PIPE, stderr=PIPE)
    # print(''.join([str(line, encoding="utf-8") for line in p.stdout.readlines()]))
    ...

"""
生成 Allure HTML报告

下载 allure-command，下载地址: https://github.com/allure-framework/allure2/releases
解压后，PATH环境变量添加 allure/bin路径

allure generate report -o html --clean
"""
