#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : sql_util.py
# @Time    : 2019/8/30 11:55
# @Author  : Kelvin.Ye
from typing import Tuple

import cx_Oracle as oracle_engine
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine.result import Result


class DBEngine:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(url)

    def execute(self, expression: str) -> Tuple[Connection, Result]:
        """执行 sql

        :param expression:  sql
        :return:            sql结果集
        """
        connection = self.engine.connect()
        result = connection.execute(expression)
        return connection, result

    def select_first(self, expression: str):
        connection, result = self.execute(expression)
        rows = result.first()
        connection.close()
        return rows

    def delete(self, expression: str):
        connection, result = self.execute(expression)
        print(result.__dict__)
        connection.close()


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


def rownum(expression: str, number: int = 1):
    """拼接SQL语句，获取指定的rownum数据

    :param expression:  sql
    :param number:      rownum
    :return:
    """
    return f'select * from ({expression}) where rownum={number}'
