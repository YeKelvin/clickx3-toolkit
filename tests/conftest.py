#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest
# @Time    : 2020/4/2 17:15
# @Author  : Kelvin.Ye
import allure
import pytest


# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     outcome = yield
#     result = outcome.get_result()
#     if result.when == 'call' and result.failed:  # 测试执行阶段且测试失败时执行以下动作
#         mode = 'a' if os.path.exists('failures') else 'w'
#         with open('failures', mode) as f:
#             if 'tmpdir' in item.fixturenames:
#                 extra = ' (%s)' % item.funcargs['tmpdir']
#             else:
#                 extra = ''
#             f.write(result.nodeid + extra + '\n')
#         with allure.step('添加失败截图...'):
#             allure.attach(driver.get_screenshot_as_png(), '失败截图', allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
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
