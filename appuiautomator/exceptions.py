#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : exceptions.py.py
# @Time    : 2019/8/30 10:51
# @Author  : Kelvin.Ye
from appuiautomator.utils.logger import get_logger

log = get_logger(__name__)


class BaseError(Exception):
    pass


class PageElementError(Exception):
    pass


class U2ClientError(BaseError):
    """Uiautomator2 Python客户端异常类
    """

    def __init__(self, msg=None) -> None:
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class ServiceError(BaseError):
    """业务异常类
    """

    def __init__(self, msg=None) -> None:
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
