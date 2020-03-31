#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : adb_test.py
# @Time    : 2019/10/10 15:42
# @Author  : Kelvin.Ye
from adbutils import adb

# ===============================================================================
# 调试adbutil
# ===============================================================================
if __name__ == '__main__':
    print(f'len={len(adb.device_list())}')
    for d in adb.device_list():
        print(d.serial)
