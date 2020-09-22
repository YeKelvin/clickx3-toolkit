#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest
# @Time    : 2020/4/2 17:15
# @Author  : Kelvin.Ye
import allure
import pytest
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     pytest_html = item.config.pluginmanager.get_plugin('html')
#     outcome = yield
#     result = outcome.get_result()
#     extra = getattr(result, 'extra', [])
#     # if result.when == 'call' and result.failed:  # 测试执行阶段且测试失败时执行以下动作
#     if result.when == 'call':  # 测试执行阶段且测试失败时执行以下动作
#         # pytest-html添加截图
#         image_name = result.nodeid.replace('::', '_') + '.png'
#         # extra.append(pytest_html.extras.image(image_name, mime_type='image/png', extension='png'))
#         extra.append(pytest_html.extras.png(image_name))
#         result.extra = extra
#         # with allure.step('添加失败截图...'):
#         #     allure.attach(driver.get_screenshot_as_png(), '失败截图', allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    print(f'item.config.option.htmlpath={item.config.option.htmlpath}')
    print(f'item.execution_count={item.execution_count}')
    print(f'result.when={result.when}')
    print(f'result.failed={result.failed}')

# def pytest_runtest_call(item):
#     print('pytest_runtest_call')
#     print(dir(item))
#     print(f'item.execution_count={item.execution_count}')


# def pytest_runtest_teardown(item):
#     print('pytest_runtest_teardown')
#     print(dir(item))
#     print(f'item.outcome={item.reportinfo()}')
