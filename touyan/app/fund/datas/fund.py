#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 16:47
# @Author  : wangyang
# @File    : fund.py
# @Software: PyCharm

from django.db.models import Max,Min
from app.fund.models import *
import datetime
import requests
import json, re
import pandas as pd

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


#获取收盘价
class GetFundClose():
    def __init__(self,code,sdate='2000-01-01'):
        self.code = code
        self.sdate = sdate

    def get_close(self):
        jjNet.objects.filter(jjcode=self.code).order_by('datadate')
        df = pd.DataFrame(list(jjNet.objects.filter(jjcode=self.code).order_by('-datadate').values()))
        if df.empty:
            return df,None
        #已有的最新日期
        exist_max_day =  df['datadate'].max()
        resp = loads_jsonp(requests.get('http://fundgz.1234567.com.cn/js/'+ self.code +'.js').content.decode(encoding='utf-8'))
        now = resp['gztime'].split(' ')[0].split('-')
        now = [int(x) for x in now]
        df = df[['datadate', 'net_value', 'sum_value']]
        df = df.set_index('datadate').sort_index()
        #如果还没开盘没有新日期，就不用这样处理
        if exist_max_day < datetime.date(now[0],now[1],now[2]):
            #虽然有分红，但是每天净值变化是一样的
            #今天的累计净值 = 昨天累计净值 + 变化
            now_sum = float(df['sum_value'][-1]) + float(resp['gsz'])-float(resp['dwjz'])
            df.loc[datetime.date(now[0],now[1],now[2])] = [round(float(resp['gsz']),4),round(now_sum,4)]
        df['net_value'] = df['net_value'] * 100
        df['sum_value'] = df['sum_value'] * 100
        df = df.sort_index()
        return df,resp['gztime']


if __name__ == '__main__':
    pass