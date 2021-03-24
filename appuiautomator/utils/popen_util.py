#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : popen_util
# @Time    : 2020/10/23 15:01
# @Author  : Kelvin.Ye
from subprocess import Popen, PIPE, STDOUT
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


def execute_command(cmd, realtime_log=False):
    """执行shell

    :param cmd:             shell
    :param realtime_log:    是否实时输出日志
    :return:                执行结果
    """
    popen = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, universal_newlines=True, encoding='utf-8')
    if realtime_log:
        lines = []
        while popen.poll() is None:  # 检查子进程是否结束
            line = popen.stdout.readline()
            line = line.strip()
            lines.append(line)
            log(line)
        if popen.returncode == 0:
            return lines
        else:
            return popen.returncode
    else:
        returncode = popen.communicate()
        if returncode == 0:
            return popen.stdout.readlines()
        else:
            return returncode
