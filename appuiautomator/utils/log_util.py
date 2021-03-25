#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : logger.py
# @Time    : 2019/8/27 13:48
# @Author  : Kelvin.Ye
import logging

from appuiautomator.utils import config


# 日志格式
LOG_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s.%(funcName)s %(lineno)d] %(message)s'

# 日志级别
LEVEL = config.get('log', 'level')

# 日志文件名称
LOG_FILE_NAME = config.get('log', 'name')

# 日志格式
FORMATTER = logging.Formatter(LOG_FORMAT)

# 输出到控制台
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)


def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(LEVEL)
    logger.addHandler(CONSOLE_HANDLER)
    return logger
