#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : logger.py
# @Time    : 2019/8/27 13:48
# @Author  : Kelvin.Ye
import logging

from logging.config import dictConfig

from clickx3.utils import project
from clickx3.utils.convert_util import str_to_bool

# 日志格式
LOG_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s.%(funcName)s %(lineno)d] %(message)s'

# 日志级别
LOG_LEVEL = project.config.get('log', 'level', default='INFO')

# 是否输出至日志文件
LOG_FILE = str_to_bool(project.config.get('log', 'file', default=False))

# 日志文件名称
LOG_FILE_NAME = project.config.get('log', 'name', default='clickx3')

# 日志格式
FORMATTER = logging.Formatter(LOG_FORMAT)

# 输出到控制台
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

# 写入日志文件
FILE_HANDLER = None

# logger配置
LOG_CONFIG = {
    'version': 1,
    'root': {
        'propagate': False,
        'level': LOG_LEVEL,  # handler的level会覆盖掉这里的level
        'handlers': ['console']
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'formatters': {
        'default': {
            'format': LOG_FORMAT
        }
    },
    'loggers': {
        'urllib3.connectionpool': {
            'level': 'ERROR'
        },
        'imageio_ffmpeg': {
            'level': 'ERROR'
        }
    }
}

if LOG_FILE:
    # 配置FileHandler
    FILE_HANDLER = logging.FileHandler(LOG_FILE_NAME, encoding='utf-8')
    FILE_HANDLER.setFormatter(FORMATTER)

    # 修改log配置，添加FileHandler
    LOG_CONFIG['root']['handlers'] = ['console', 'file']
    LOG_CONFIG['handlers']['file'] = {
        'class': 'logging.FileHandler',
        'formatter': 'default',
        'encoding': 'utf-8',
        'filename': LOG_FILE_NAME
    }

dictConfig(LOG_CONFIG)


def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(CONSOLE_HANDLER)
    if LOG_FILE and FILE_HANDLER:
        logger.addHandler(FILE_HANDLER)
    return logger
