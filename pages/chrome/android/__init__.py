#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2020/9/17 14:39
# @Author  : Kelvin.Ye

"""
Chrome App
"""

from appuiautomator.u2.app import AndroidApp
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class Chrome(AndroidApp):
    package_name = 'com.android.chrome'
    activity_name = 'com.google.android.apps.chrome.Main'
