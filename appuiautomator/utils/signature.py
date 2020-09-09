#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : http_sign
# @Time    : 2020/9/8 15:20
# @Author  : Kelvin.Ye
from appuiautomator.utils.dict_util import sort_dict
from appuiautomator.utils.logger import get_logger
from appuiautomator.utils.md5_util import md5

log = get_logger(__name__)


def traverse(buffer: list, key: str, value: object):
    if isinstance(value, dict):
        buffer.append(f'{key}={traverse_dict(value)}&')
    elif isinstance(value, list):
        buffer.append(f'{key}={traverse_list(value)}&')
    elif isinstance(value, bool):
        buffer.append(f'{key}={str(value).lower()}&')
    elif value is None:
        buffer.append(f'{key}=null&')
    else:
        buffer.append(f'{key}={str(value)}&')


def traverse_dict(obj: dict):
    if not obj:
        return '{}'
    sorted_dict = sort_dict(obj)
    if not sorted_dict:
        return '{}'
    buffer = ['{']
    for key, value in sorted_dict.items():
        traverse(buffer, key, value)
    return (''.join(buffer))[0:-1] + '}'


def traverse_list(obj: list):
    if not obj:
        return '[]'
    buffer = ['[']
    for item in obj:
        if isinstance(item, dict):
            buffer.append(traverse_dict(item))
        elif isinstance(item, list):
            buffer.append(traverse_list(item))
        else:
            buffer.append(str(item))
        buffer.append(',')
    return (''.join(buffer))[0:-1] + ']'


def sign(req):
    if not req:
        return ''
    sorted_dict = sort_dict(req)
    if not sorted_dict:
        return ''
    buffer = []
    for key, value in sorted_dict.items():
        traverse(buffer, key, value)
    if not buffer:
        return ''
    sign_str = (''.join(buffer))[0:-1]
    log.debug(f'sign before: {sign_str}')
    return md5(sign_str)


if __name__ == '__main__':
    req = {'name': 'laohu', 'age': {'aa': 'aa', 'bb': 33}, 'length': [1.01, 2, 3, 4]}
    sign = sign(req)
    print(sign)
