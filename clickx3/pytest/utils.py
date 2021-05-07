#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : utils.py
# @Time    : 2021/5/6 18:27
# @Author  : Kelvin.Ye
import os


def node_id_to_name(nodeid):
    formatted_nodeid = nodeid.replace('.py', '').replace('::', '.')
    if os.sep in formatted_nodeid:
        return formatted_nodeid.split(os.sep)[-1]
    else:
        return formatted_nodeid.split('/')[-1]
