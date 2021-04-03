#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2020/9/1 16:16
# @Author  : Kelvin.Ye

"""
demo
"""

from appuiautomator.action import BaseAction
from appuiautomator.u2.app import App
from appuiautomator.utils.log_util import get_logger
from example.pages.app_name.first import FirstPage
from example.pages.app_name.second import SecondPage

log = get_logger(__name__)


class Action(BaseAction):
    def __init__(self, source: 'ApplicationName'):
        self.source = source

    def do_action(self):
        self.source.first_page.do_something()
        self.source.second_page.do_something()


class ApplicationName(App):
    """App子类"""
    action = Action()
    package_name = 'app.name'

    first_page = FirstPage()
    second_page = SecondPage()
