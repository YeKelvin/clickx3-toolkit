#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : jsonpath_util.py
# @Time    : 2019/9/7 18:05
# @Author  : Kelvin.Ye
import orjson
from typing import Union

from jsonpath import jsonpath


def to_json(obj: Union[dict, list]) -> str:
    """序列化
    """
    return orjson.dumps(obj)


def from_json(json_text: str) -> Union[dict, list]:
    """反序列化
    """
    return orjson.loads(json_text)


def extract_json(json_text: str, json_path: str):
    """根据 JsonPath提取字段值
    """
    result_list = jsonpath(from_json(json_text), json_path)
    if len(result_list) == 1:
        return result_list[0]
    return result_list
