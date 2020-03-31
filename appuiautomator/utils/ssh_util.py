#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ssh_util.py
# @Time    : 2019/8/30 11:52
# @Author  : Kelvin.Ye
from sshtunnel import SSHTunnelForwarder


def local_port_forwarding(ssh_address: str,
                          ssh_username: str,
                          ssh_password: str,
                          local_bind_address: str,
                          remote_bind_address: str) -> SSHTunnelForwarder:
    """本地端口转发
    地址统一格式为 ip:port

    :param ssh_address:         跳板机地址
    :param ssh_username:        跳板机用户名
    :param ssh_password:        跳板机密码
    :param local_bind_address:  本地地址
    :param remote_bind_address: 远程地址
    :return:
    """
    ssh_client = SSHTunnelForwarder(ssh_address_or_host=_address_to_tuple(ssh_address),
                                    ssh_username=ssh_username,
                                    ssh_password=ssh_password,
                                    local_bind_address=_address_to_tuple(local_bind_address),
                                    remote_bind_address=_address_to_tuple(remote_bind_address))
    return ssh_client


def _address_to_tuple(address: str) -> tuple:
    colon_index = address.index(':')
    return address[:colon_index], int(address[colon_index + 1:])
