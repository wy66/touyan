#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 15:51
# @Author  : wangyang
# @File    : util.py
# @Software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ttjj.settings import *
from contextlib import contextmanager
from collections import defaultdict


engine = create_engine("mysql+pymysql://{name}:{pwd}@{host}:3306/{db}".
                       format(name=MYSQL_USER, pwd=MYSQL_PASSWD, host=MYSQL_HOST, db=MYSQL_DBNAME),
                       echo=True, encoding='utf-8', convert_unicode=True)
# echo=True 显示信息
Base = declarative_base()  # 生成orm基类
Session_class = sessionmaker(bind=engine)
session = Session_class()  # 生成session实例


@contextmanager
def session_maker(session=session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict(table):
    result = defaultdict(lambda: defaultdict())
    for row_i, row in enumerate(table.xpath('./tbody/tr|./tr')):
        #         print row
        for col_i, col in enumerate(row.xpath('./td|./th')):
            #             print col
            try:
                colspan = int(col.xpath('./@colspan').extract_first().strip())
            except:
                colspan = 1
            try:
                rowspan = int(col.xpath('./@rowspan').extract_first().strip())
            except:
                rowspan = 1
            col_data = ''.join(col.xpath('.//text()').extract()).strip()
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data

    return result


def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


def table_to_list2(table):
    dct = table_to_2d_dict2(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict2(table):
    result = defaultdict(lambda: defaultdict())
    for row_i, row in enumerate(table.xpath('./tr|./tbody/tr')):
        istable = False
        rowspan = 0
        for col_i, col in enumerate(row.xpath('./td|./th')):
            if col.xpath('.//tr'):
                rowspan = len(col.xpath('.//tr'))
                istable = True

        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            if not istable:
                rowspan = int(col.get('rowspan', 1))
            # 郑商所仓单特殊情况
            if col.xpath('.//tr'):
                while row_i in result and col_i in result[row_i]:
                    col_i += 1
                for row_i_2, row_2 in enumerate(col.xpath('.//tr|./tbody//tr')):
                    for col_i_2, col_2 in enumerate(row_2.xpath('./td|./th')):
                        colspan_2 = int(col_2.get('colspan', 1))
                        rowspan_2 = int(col_2.get('rowspan', 1))
                        while row_i + row_i_2 in result and col_i + col_i_2 in result[row_i + row_i_2]:
                            col_i_2 += 1
                        col_data = col_2.text_content()
                        for i_2 in range(row_i + row_i_2, row_i + row_i_2 + rowspan_2):
                            for j_2 in range(col_i + col_i_2, col_i + col_i_2 + colspan_2):
                                result[i_2][j_2] = col_data
            else:
                col_data = col.text_content()
                while row_i in result and col_i in result[row_i]:
                    col_i += 1
                for i in range(row_i, row_i + rowspan):
                    for j in range(col_i, col_i + colspan):
                        result[i][j] = col_data
    return result
