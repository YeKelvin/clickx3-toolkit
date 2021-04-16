#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : excel_util
# @Time    : 2020/9/10 14:14
# @Author  : Kelvin.Ye
import xlwings as xw


def read_excel_demo(excel_file, sheet_name):
    wb = xw.Book(excel_file)
    sheet = wb.sheets[sheet_name]
    used_range = sheet.used_range
    start_row = 2
    end_row = used_range.last_cell.row
    end_column = used_range.last_cell.column
    rows = []

    for row in range(start_row, end_row):
        row_values = []
        # a-z:97-122，AZ:65-90
        for column in range(0, end_column - 1):
            column_chr = chr(65 + column)
            row_values.append(sheet.range(f'{column_chr}{row}').value)

    for row in rows:
        print(row)
