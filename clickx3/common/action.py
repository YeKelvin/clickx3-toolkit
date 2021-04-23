#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : action.py
# @Time    : 2021/04/01 13:44
# @Author  : Kelvin.Ye


class BaseAction:

    def __init__(self, app=None):
        self.app = app

    def __get__(self, instance, owner):
        if instance is None:
            raise Exception('持有类必须实例化')
        if self.app is None:
            self.app = instance
        return self

    def __set__(self, instance, value):
        raise NotImplementedError('用不着')
