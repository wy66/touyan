#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 15:42
# @Author  : wangyang
# @File    : models.py
# @Software: PyCharm
from ttjj.util import Base,engine
from sqlalchemy import Column, Integer, String,DateTime,DECIMAL,UniqueConstraint,Index,Float,func


class TtjjCodeModel(Base):
    __tablename__ = 'TtjjCode'

    jjcode =  Column(String(20),primary_key=True)
    fname =  Column(String(200))
    sname =  Column(String(100))
    stype = Column(String(50))
    sday = Column(DateTime)
    gm = Column(Float)
    insert_dt = Column(DateTime, server_default=func.now())
    update_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint('jjcode',name='ttjj_code_index'),
    )

class TtjjNetModel(Base):
    __tablename__ = 'TtjjNet'

    datadate = Column(DateTime,primary_key=True)
    jjcode =  Column(String(20),primary_key=True)
    net_value =  Column(Float)
    sum_value =  Column(Float)

    __table_args__ = (
        UniqueConstraint('datadate','jjcode', name='ttjj_net_index'),
    )

class TtjjTop10StockModel(Base):
    __tablename__ = 'TtjjTop10Stock'

    datadate = Column(DateTime,primary_key=True)
    jjcode =  Column(String(20),primary_key=True)
    scode = Column(String(30), primary_key=True)
    sname =  Column(String(100))
    pct = Column(Float)
    num = Column(Float)

    __table_args__ = (
        UniqueConstraint('datadate','jjcode','scode', name='ttjj_top10_stock_index'),
    )

if __name__ == '__main__':
    Base.metadata.create_all(engine)
