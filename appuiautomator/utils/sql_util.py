#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : sql_util.py
# @Time    : 2019/8/30 11:55
# @Author  : Kelvin.Ye
from typing import Tuple

import cx_Oracle as oracle_engine
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine.result import ResultProxy


class SQL:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(url)

    def execute(self, expression: str) -> Tuple[Connection, ResultProxy]:
        """执行 sql

        :param expression:  sql
        :return:            sql结果集
        """
        connection = self.engine.connect()
        result_proxy = connection.execute(expression)
        return connection, result_proxy

    def select_first(self, expression: str):
        connection, result_proxy = self.execute(expression)
        rows = result_proxy.first()
        connection.close()
        return rows


class Oracle:
    def __init__(self, username: str, password: str, address: str):
        self.username = username
        self.password = password
        self.address = address

    def select_all(self, expression: str):
        db = oracle_engine.connect(self.username, self.password, self.address)
        cur = db.cursor()
        cur.execute(expression)
        rows = cur.fetchall()
        cur.close()
        db.close()
        return rows


def rownum(expression: str, number: int):
    """拼接SQL语句，获取指定的rownum数据

    :param expression:  sql
    :param number:      rownum
    :return:
    """
    return f'select * from ({expression}) where rownum={number}'
