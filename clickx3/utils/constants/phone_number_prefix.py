#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : phone_number_prefix.py
# @Time    : 2019/8/30 15:22
# @Author  : Kelvin.Ye
from itertools import chain


# 移动
CMCC_CODE = ['134', '135', '136', '137', '138', '139', '147', '150', '151', '152', '157', '158', '159', '170',
             '172', '178', '182', '183', '184', '187', '188']
# 联通
CUCC_CODE = ['130', '131', '132', '145', '155', '156', '170', '171', '175', '176', '185', '186']

# 电信
TELECOM_CODE = ['133', '149', '153', '158', '170', '173', '177', '178', '180', '181', '182', '189', '199']

# 手机号运营商前缀
MOBILENO_PREFIX = list(chain(CMCC_CODE, CUCC_CODE, TELECOM_CODE))
