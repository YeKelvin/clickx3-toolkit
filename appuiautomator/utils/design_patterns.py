#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : design_patterns.py
# @Time    : 2019/10/16 11:55
# @Author  : Kelvin.Ye

# ===============================
# 设计模式
# ===============================
import threading


class Singleton:
    """单例模式
    """
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance
