#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 16:47
# @Author  : wangyang
# @File    : fund.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod
from jqdatasdk import *

#auth('14613350695', '350695')
JQUER = '14613350695'
JQPWD  = '350695'

#获取基金的收盘价
class GetFundClose(metaclass=ABCMeta):
    @abstractmethod
    def get_close(self):  # 制定了一个规范
        pass

#聚宽数据
class GetFundCloseJq(GetFundClose):
    def __init__(self,code,sdate):
        self.code = code
        self.sdate = sdate
    def get_close(self):
        auth(JQUER,JQPWD)
        #获取所有
        df = get_all_securities(['fund'])
        get_security_info(self.code, date=None)

