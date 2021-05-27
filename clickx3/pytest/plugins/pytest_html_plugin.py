#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pytest_html_plugin.py
# @Time    : 2021/5/1 11:24
# @Author  : Kelvin.Ye
import pytest
from py._xmlgen import html


@pytest.mark.optionalhook
def pytest_html_report_title(report):
    """编辑报告标题"""
    report.title = 'APP UI自动化测试报告'


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    """编辑表格头部"""
    cells.pop(-1)  # 删除Links列
    cells.insert(1, html.th('Description'))  # 添加Description列


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """编辑表格主体"""
    cells.pop(-1)  # 删除Links列
    cells.insert(1, html.td(report.description))  # 添加Description列


def pytest_runtest_makereport(item, result):
    """编辑测试报告"""
    result.description = str(item.function.__doc__)  # 添加测试用例描述
    result.nodeid = result.nodeid.encode('utf-8').decode('unicode_escape')  # 解决中文乱码
    setattr(result, "duration_formatter", "%H:%M:%S.%f")
