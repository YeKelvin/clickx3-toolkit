#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : logger.py
# @Time    : 2019/8/27 13:48
# @Author  : Kelvin.Ye
import logging

# from clickx3.utils import config
from clickx3.utils import project


# 日志格式
LOG_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s.%(funcName)s %(lineno)d] %(message)s'

# 日志级别
# LEVEL = config.get('log', 'level')
LEVEL = project.config.get('log', 'level')

# 日志文件名称
# LOG_FILE_NAME = config.get('log', 'name')
LOG_FILE_NAME = project.config.get('log', 'level')

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
