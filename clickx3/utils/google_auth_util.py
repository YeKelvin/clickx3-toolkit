#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : google_auth_util.py
# @Time    : 2021/04/19 15:55
# @Author  : Kelvin.Ye

"""
Google Authenticator
"""

import base64
import hashlib
import hmac
import struct
import time
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


def get_google_captcha_code(secret_key):
    log.info(f'谷歌验证码秘钥:[ {secret_key} ]')

    key = base64.b32decode(secret_key, True)
    intervals_no = int(time.time()) // 30
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    captcha_code = '%06d' % h

    log.info(f'谷歌验证码:[ {captcha_code} ]')
    return captcha_code
