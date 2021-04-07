#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : wda_test.py
# @Time    : 2020/4/2 16:14
# @Author  : Kelvin.Ye
import wda


def test_wda():
    s = wda.Client().session()
    print(s)


if __name__ == '__main__':
    ...
