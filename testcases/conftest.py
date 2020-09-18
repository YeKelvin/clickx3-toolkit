#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest.py
# @Time    : 2020/9/16 16:09
# @Author  : Kelvin.Ye
import pytest

from appuiautomator.devices_manager import DevicesManager
from appuiautomator.u2 import device
from appuiautomator.u2.device import Device


@pytest.fixture(scope='session')
def an_serial():
    return DevicesManager.android().get_device()


@pytest.fixture(scope='session')
def an_device(an_serial):
    return Device(device.connect(an_serial))


@pytest.fixture(scope='session')
def ios_serial():
    ...
