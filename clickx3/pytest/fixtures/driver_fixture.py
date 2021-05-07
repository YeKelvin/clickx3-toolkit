#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : driver_fixture.py
# @Time    : 2021/5/1 13:39
# @Author  : Kelvin.Ye
import pytest

from clickx3.se.driver import Driver


@pytest.fixture(scope='session')
def chrome_driver(headless):
    driver = Driver.chrome(headless=headless)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='session')
def firefox_driver(headless):
    driver = Driver.firefox(headless=headless)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='session')
def edge_driver(headless):
    driver = Driver.edge()(headless=headless)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='session')
def web_driver(chrome_driver):
    return chrome_driver
