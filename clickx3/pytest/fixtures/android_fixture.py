#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : android_fixture.py
# @Time    : 2021/5/6 17:16
# @Author  : Kelvin.Ye
import pytest

from clickx3.common.devices_manager import DevicesManager
from clickx3.u2.device import Device


@pytest.fixture(scope='session')
def android_serial():
    return DevicesManager.android().get_device()


@pytest.fixture(scope='session')
def android_device(android_serial):
    return Device.connect(android_serial)


@pytest.fixture(scope='session')
def chrome_webview(android_device):
    from apps.chrome.android import Chrome
    return Chrome(android_device).webview
