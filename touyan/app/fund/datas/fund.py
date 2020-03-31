#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 16:47
# @Author  : wangyang
# @File    : fund.py
# @Software: PyCharm

######加载django环境
import os
import django
# 添加环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "touyan.settings")
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()


from app.fund.models import *
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



#获取聚宽所以代码
def get_jq_code():
    auth('14613350695', '350695')
    df = get_all_securities(types=['fund', 'index', 'etf', 'lof', 'QDII_fund', 'stock_fund', 'mixture_fund', 'open_fund'],
        date='2020-03-26')

    for i,row in df.iterrows():
        print(i)
        try:
            JqCodeInfo.objects.create(
                code=i.split('.')[0],
                name = row['display_name'],
                short_name = row['name'],
                sdate = row['start_date'],
                edate = row['end_date'],
                type = row['type']
            )
        except Exception as e:
            if 'UNIQUE constraint' in e.args[0]:
                pass
            else:
                print(e)


if __name__ == '__main__':
    get_jq_code()