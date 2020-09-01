#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2020/9/1 16:39
# @Author  : Kelvin.Ye

"""
Via App
"""

from appuiautomator.u2.app import App
from appuiautomator.utils.logger import get_logger
from pages.via.home import HomePage

log = get_logger(__name__)


class Via(App):
    package_name = 'mark.via'

    home_page = HomePage()
