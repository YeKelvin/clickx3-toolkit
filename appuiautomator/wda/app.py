#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app
# @Time    : 2020/4/3 19:14
# @Author  : Kelvin.Ye


class App:
    bundle_id = ''

    def __init__(self, device):
        self.device = device
        self.session = device.session
