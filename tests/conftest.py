#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest
# @Time    : 2020/4/2 17:15
# @Author  : Kelvin.Ye
import os

import allure
import pytest

# driver = None
#
#
# @pytest.mark.hookwrapper
# def screenshot_on_test_failed(item):
#     outcome = yield
#     rep = outcome.get_result()
#     if rep.when == 'call' and rep.failed:
#         mode = 'a' if os.path.exists('failures') else 'w'
#         with open('failures', mode) as f:
#             if 'tmpdir' in item.fixturenames:
#                 extra = ' (%s)' % item.funcargs['tmpdir']
#             else:
#                 extra = ''
#             f.write(rep.nodeid + extra + '\n')
#         with allure.step('添加失败截图...'):
#             allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


# @pytest.fixture(scope='session', autouse=True)
# def browser():
#     global driver
#     if driver is None:
#         driver = webdriver.Chrome()
#     return driver
