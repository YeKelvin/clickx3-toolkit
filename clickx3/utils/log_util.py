#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : logger.py
# @Time    : 2019/8/27 13:48
# @Author  : Kelvin.Ye
import logging
from logging.config import dictConfig

from clickx3.utils import project

# 日志格式
LOG_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s.%(funcName)s %(lineno)d] %(message)s'

# 日志级别
LOG_LEVEL = project.config.get('log', 'level')

# 日志文件名称
LOG_FILE_NAME = project.config.get('log', 'name')

# 日志格式
FORMATTER = logging.Formatter(LOG_FORMAT)

# 输出到控制台
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

# logger配置
dictConfig({
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
})


def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(CONSOLE_HANDLER)
    return logger
