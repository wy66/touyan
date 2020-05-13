# -*- coding: utf-8 -*-
import scrapy
import re
import json
import math
import datetime
from ttjj.items import *
from ttjj.util import table_to_list

#获取净值的开始时间
NET_SDAY = '2017-01-01'
#净值每次取得条数
NET_NUM = 300


class TtjjNetSpider(scrapy.Spider):
    name = 'ttjj_net'
    allowed_domains = []
    start_urls = ['http://fund.eastmoney.com/js/fundcode_search.js']

    #获取基金列表
    def parse(self, response):
        for row in eval(response.text[8:-1]):
            yield scrapy.Request(url='http://fundf10.eastmoney.com/{code}.html'.format(code=row[0]), callback=self.parse1, meta={'code':row[0]})

    #获取每个基金对应信息
    def parse1(self,response):
        eles = response.xpath('//table[@class="info w790"]')

        if len(eles) > 0:
            table = table_to_list(eles[0])
            code = response.meta.get('code')
            fname = table[0][1]
            sname = table[0][3]
            stype = table[1][3]
            tmp = re.findall(r'\d+',table[2][3])
            sday = datetime.datetime.strptime(str(tmp[0])+'-'+ str(tmp[1]) + '-' + str(tmp[2]) ,'%Y-%m-%d')
            gm = table[3][1]
            if '亿' not in gm:
                return
            gm = re.findall(r'\d+',gm)[0]
            #只取规模大于5亿元
            if float(gm) < 2:
                return
            #持有一般都有封闭期
            if '持有' in fname or '封闭' in fname or '定期' in fname:
                return
            #乱七八糟不要
            if stype in ['货币型', '债券型', '定开债券', '固定收益', '理财型', '分级杠杆', '其他创新']:
                return

            item = TtjjCode()
            item['jjcode'] = code
            item['fname'] = fname
            item['sname'] = sname
            item['stype'] = stype
            item['sday'] = sday
            item['gm'] = gm
            yield item

            #持仓股票
            url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={code}&topline=10'.format(code = code)
            yield scrapy.Request(url=url, callback=self.parse3, meta={'code': code})
            #基金净值
            url = 'http://api.fund.eastmoney.com/f10/lsjz?fundCode={code}&pageIndex=1&pageSize={num}&startDate={sday}&endDate='.format(code=code,num=NET_NUM,sday=NET_SDAY)
            yield scrapy.Request(url=url, callback=self.parse2, meta={'code':code,'flag':1})

    #获取基金净值
    def parse2(self,response):
        code = response.meta.get('code')
        flag = response.meta.get('flag')
        #第一次，需要获取页数，方便对剩下的数据获取
        data = json.loads(response.text)
        if flag == 1:
            table = data['Data']['LSJZList']
            for row in table:
                item = TtjjNet()
                item['datadate'] = datetime.datetime.strptime(row['FSRQ'] ,'%Y-%m-%d')
                item['jjcode'] = code
                item['net_value'] = row['DWJZ'] if row['DWJZ'] != '' else None
                item['sum_value'] = row['LJJZ'] if row['LJJZ'] != '' else None
                yield item

            pages = math.ceil(data['TotalCount']/NET_NUM)
            if pages > 1:
                for p in range(2,pages+1):
                    url = 'http://api.fund.eastmoney.com/f10/lsjz?fundCode={code}&pageIndex={page}&pageSize={num}&startDate={sday}&endDate='.format(code = code,page=p,num=NET_NUM,sday=NET_SDAY)
                    yield scrapy.Request(url=url, callback=self.parse2, meta={'code': code, 'flag': 2})

        elif flag == 2:
            table = data['Data']['LSJZList']
            for row in table:
                item = TtjjNet()
                item['datadate'] = datetime.datetime.strptime(row['FSRQ'], '%Y-%m-%d')
                item['jjcode'] = code
                item['net_value'] = row['DWJZ'] if row['DWJZ'] != '' else None
                item['sum_value'] = row['LJJZ'] if row['LJJZ'] != '' else None
                yield item

    #获取基金十大股票持仓
    def parse3(self,response):
        code = response.meta.get('code')
        day = response.xpath('//font/text()').extract()
        if len(day) == 0:
            return
        day = day[0]
        table = table_to_list(response.xpath('//table')[0])
        for row in table:
            item = TtjjTop10Stock()
            item['datadate'] = datetime.datetime.strptime(day, '%Y-%m-%d')
            item['jjcode'] = code
            item['scode'] = row[1]
            item['sname'] = row[2]
            item['pct'] = row[6].replace('%','') if row[6] != '' else None
            item['num'] = row[7].replace(',','') if row[7] != '' else None
            yield item
