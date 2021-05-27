#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2021/4/28 11:10
# @Author  : Kelvin.Ye
from . import android_screenrecord_plugin  # noqa
from . import android_screenshot_plugin  # noqa
from . import ios_screenshot_plugin  # noqa
from . import pytest_html_plugin  # noqa
from . import web_screenrecord_plugin  # noqa
from . import web_screenshot_plugin  # noqa


__all__ = ['pytest_html_plugin']
