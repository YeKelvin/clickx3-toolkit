#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : http_client
# @Time    : 2020/9/8 15:19
# @Author  : Kelvin.Ye
import requests

from clickx3.utils.log_util import get_logger


log = get_logger(__name__)

if __name__ == '__main__':
    headers = {}
    cookies = {}
    payload = None

    res_get = requests.get(url='http://httpbin.org/get', params=payload, headers=headers, cookies=cookies)
    print(f'url={res_get.url}')
    print(f'status_code={res_get.status_code}')
    print(f'ok={res_get.ok}')
    print(f'headers={res_get.headers}')
    print(f'text={res_get.text}')
    print(f'content={res_get.content}')
    print(f'json={res_get.json()}')
    print(f'elapsed={res_get.elapsed}')
    res_get.raise_for_status()

    res_post = requests.post(url='http://httpbin.org/post', data=payload, headers=headers, cookies=cookies)
    print(f'url={res_post.url}')
    print(f'status_code={res_post.status_code}')
    print(f'ok={res_post.ok}')
    print(f'headers={res_post.headers}')
    print(f'text={res_post.text}')
    print(f'content={res_post.content}')
    print(f'json={res_post.json()}')
    print(f'elapsed={res_post.elapsed}')
    res_post.raise_for_status()
