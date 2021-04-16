#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : jsonpath_util.py
# @Time    : 2019/9/7 18:05
# @Author  : Kelvin.Ye
import orjson

from jsonpath import jsonpath


def to_json(obj):
    """序列化
    """
    return str(orjson.dumps(obj), encoding='utf-8')


def from_json(json: str):
    """反序列化
    """
    return orjson.loads(json)


def extract_json(json: str, json_path: str):
    """根据 JsonPath提取字段值
    """
    result_list = jsonpath(from_json(json), json_path)
    if len(result_list) == 1:
        return result_list[0]
    return result_list
