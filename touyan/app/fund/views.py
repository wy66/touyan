from django.shortcuts import render,HttpResponse
from django.db import connections
from .models import *
import json
import decimal
import pandas as pd
from .datas.fund import *
# Create your views here.

class JsonCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, pd.datetime):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return super(JsonCustomEncoder, self).default(obj)

def wg_add(request):
    code = request.POST.get('code')
    sdate = request.POST.get('sdate')
    try:
        OuterFundWgConf.objects.create(code = code,sdate = sdate)
    except Exception as e:
        if 'UNIQUE constraint' in e.args[0]:
            return HttpResponse(json.dumps({'errCode':500,'errMsg':'代码已存在！'}, cls=JsonCustomEncoder), 'content_type="application/json"')

    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success'}, cls=JsonCustomEncoder), 'content_type="application/json"')

def wg_query(request):
    codes = OuterFundWgConf.objects.all()
    data = {}
    for c in codes:
        data[c.code] = {}
        obj = GetFundCloseJq(c.code,sdate='2018-01-01')
        #获取基金单位净值，累计净值，变化
        df,nowtime = obj.get_close()
        # data[c.code]['data'] = ret_data
        data[c.code]['nowtime'] = nowtime
        #基准日
        base_day = c.sdate
        data[c.code]['base_day'] = base_day
        #基础净值
        base_data= df.loc[df.index==base_day]
        base_value = base_data['sum_value'].values[0]
        data[c.code]['base_value'] = base_value

        #每次涨跌步长 取5%
        rank_down = round(base_data['net_value'].values[0] * 0.05,2)

        max = df['sum_value'].max()
        min = df['sum_value'].min()
        markline = []
        temp = base_value
        while temp > min-rank_down:
            markline.append(temp - rank_down)
            temp = temp - rank_down
        temp = base_value
        while temp < max+rank_down:
            markline.append(temp + rank_down)
            temp = temp + rank_down
        data[c.code]['markline'] = markline
        data[c.code]['name'] = JqCodeInfo.objects.filter(code=c.code)[0].short_name
        data[c.code]['data'] = df.reset_index().fillna('').to_dict(orient='list')

        #捕捉买点卖点，从基准点开始
        points_list = []
        points = {}
        df1 = df.loc[df.index >= base_day]
        for d,row in df1.iterrows():
            #初始，第一天买入
            if not points:
                points['day'] = d
                points['sum_value'] = row['sum_value']
                points['act'] = 'buy'
                points_list.append(points)
            else:
                #不是第一次买入，就开始比较每天的涨跌幅
                chg = row['sum_value'] - points['sum_value']
                #跌
                if chg < 0:
                    #跌的多于步长
                    if abs(chg) > rank_down:
                        points['day'] = d
                        points['sum_value'] = row['sum_value']
                        points['act'] = 'buy'
                        points_list.append(points)
                    #跌，但是跌的少
                    else:
                        pass
                else:
                    if chg > rank_down:
                        points['day'] = d
                        points['sum_value'] = row['sum_value']
                        points['act'] = 'sale'
                        points_list.append(points)

    print(json.dumps(points_list, cls=JsonCustomEncoder))
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','data':data}, cls=JsonCustomEncoder), 'content_type="application/json"')


