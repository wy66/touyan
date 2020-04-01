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
from jqdatasdk import finance
import datetime
import requests
import json, re

#auth('14613350695', '350695')
JQUER = '14613350695'
JQPWD  = '350695'

#解析jsonp
def loads_jsonp(_jsonp):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
        except:
            raise ValueError('Invalid Input')

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
        q = query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code == self.code).order_by(finance.FUND_NET_VALUE.day.desc()).limit(1000)
        df = finance.run_query(q)

        resp = loads_jsonp(requests.get('http://fundgz.1234567.com.cn/js/'+ self.code +'.js').content.decode(encoding='utf-8'))
        now = resp['gztime'].split(' ')[0].split('-')
        now = [int(x) for x in now]
        #虽然有分红，但是每天净值变化是一样的
        df = df[['day','net_value','sum_value']]
        df = df.set_index('day').sort_index()
        #今天的累计净值 = 昨天累计净值 + 变化
        now_sum = float(df['sum_value'][-1]) + float(resp['gsz'])-float(resp['dwjz'])
        df.loc[datetime.date(now[0],now[1],now[2])] = [round(float(resp['gsz']),4),round(now_sum,4)]
        df['net_value'] = df['net_value'] * 100
        df['sum_value'] = df['sum_value'] * 100
        df = df.sort_index()
        df['chg'] = df['sum_value'] - df['sum_value'].shift(-1)

        return df,resp['gztime']

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
                jqcode= i,
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