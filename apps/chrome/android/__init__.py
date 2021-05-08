#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2021/4/28 11:10
# @Author  : Kelvin.Ye
from clickx3.u2.app import AndroidApp
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class Chrome(AndroidApp):
    package_name = 'com.android.chrome'
    activity_name = 'com.google.android.apps.chrome.Main'
