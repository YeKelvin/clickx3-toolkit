#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : randoms.py
# @Time    : 2019/8/30 15:13
# @Author  : Kelvin.Ye
import time
import random
from random import randint, choice
from datetime import date, timedelta
from appuiautomator.utils.idcard import AREA_CODE, WEIGHT, CHECK_CODE
from appuiautomator.utils.phone_number_prefix import MOBILENO_PREFIX, CMCC_CODE, CUCC_CODE, TELECOM_CODE


def get_number(length: int, prefix: str = '', suffix: str = '') -> str:
    """根据前缀、后缀和长度生成随机数

    :param length:  随机数的长度
    :param prefix:  前缀
    :param suffix:  后缀
    :return:        随机数
    """
    number = []
    for x in range(length):
        number.append(str(randint(0, 9)))
    return prefix.join(number).join(suffix)


def get_idcard():
    """生成随机身份证号码
    """
    idcard = AREA_CODE[randint(0, len(AREA_CODE))]['code']  # 地区项
    idcard += str(randint(1930, 2018))  # 年份项
    da = date.today() + timedelta(days=randint(1, 366))  # 月份和日期项
    idcard += da.strftime('%m%d')
    idcard += str(randint(100, 300))  # 顺序号
    count = 0

    for i in range(0, len(idcard)):
        count += int(idcard[i]) * WEIGHT[i]
        idcard = idcard + CHECK_CODE[str(count % 11)]  # 算出校验码
        return idcard


def get_bankcard(cardbin, length) -> str:
    """根据卡bin和卡长度随机生成银行卡卡号。

    :param cardbin:     卡bin
    :param length:      卡长度
    :return:            银行卡卡号
    """
    if length < len(cardbin):
        raise Exception('长度不能小于cardBin的长度')
    return get_number(length - len(cardbin), prefix=str(cardbin))


def get_phone_number(operators='ALL'):
    """生成随机手机号

    :param operators:   通讯运营商，默认ALL，可选 CMCC | CUCC | TELECOM
    :return:            手机号
    """
    return {
               'ALL': choice(MOBILENO_PREFIX),
               'CMCC': choice(CMCC_CODE),
               'CUCC': choice(CUCC_CODE),
               'TELECOM': choice(TELECOM_CODE)
           }.get(operators, choice(MOBILENO_PREFIX)) + get_number(8)


def get_phone_number_cambodia():
    """随机生成855可用运营商号段注册号码
    """
    phone_list = ['11', '12', '17', '61', '76', '77', '78', '79', '85', '89', '92',
                  '95', '99', '10', '15', '16', '69', '70', '81', '86', '87', '93',
                  '96', '98', '31', '60', '66', '67', '68', '71', '88', '90', '97',
                  '13', '80', '83', '84', '38', '18'
                  ]  # 柬埔寨可正常使用手机号号段
    num_length = random.randint(6, 7)
    register_number = random.choice(phone_list) + "".join(random.choice("0123456789") for i in range(num_length))
    return register_number


def now() -> str:
    """获取当前时间
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_logid(prefix: str = '', suffix: str = '') -> str:
    """获取日志id

    :param prefix:  前缀
    :param suffix:  后缀
    :return:        日志id
    """
    return prefix + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + get_number(6) + suffix
