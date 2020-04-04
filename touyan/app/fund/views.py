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


#计算macd
def wg_macd(df):
    #计算说明 https://blog.csdn.net/daodan988/article/details/51258676
    macd  ={'diff':[],'dea':[],'bar':[],'day':[]}
    pre_close = None
    pre_EMA_12 = None
    pre_EMA_26 = None
    pre_dea = None
    for day,row in df.iterrows():
        if pre_close is None:
            pre_close = row['sum_value']
            macd['diff'].append('')
            macd['dea'].append('')
            macd['bar'].append('')
            macd['day'].append('')
            continue
        elif pre_EMA_12 is None:
            pre_EMA_12 = pre_close + (row['sum_value'] - pre_close) * 2.0 / 13
            pre_EMA_26 = pre_close + (row['sum_value'] - pre_close) * 2.0 / 27
            diff = pre_EMA_12 - pre_EMA_26
            dea = 0 + diff * 2.0 / 10
            pre_dea = dea
            bar = 2.0 * (diff - dea)
            macd['diff'].append(diff)
            macd['dea'].append(dea)
            macd['bar'].append(bar)
            macd['day'].append(day)
        else:
            EMA_12 = pre_EMA_12 * 11.0 / 13 + row['sum_value'] * 2.0 / 13
            pre_EMA_12 = EMA_12
            EMA_26 = pre_EMA_26 * 25.0 / 27 + row['sum_value'] * 2.0 / 27
            pre_EMA_26 = EMA_26
            diff = EMA_12 - EMA_26
            dea = pre_dea * 8.0 / 10  + diff * 2.0 /10
            pre_dea = dea
            bar = 2.0 * (diff - dea)
            macd['diff'].append(diff)
            macd['dea'].append(dea)
            macd['bar'].append(bar)
            macd['day'].append(day)

    return macd

#根据第一次买入日期计算后面网格操作
def wg_act(df,code,sdate):
    act = {}



def wg_query(request):
    code = request.POST.get('code')
    sdate = request.POST.get('sdate')
    name = request.POST.get('name')
    data = {}

    obj = GetFundCloseJq(code,sdate='2018-01-01')

    #获取基金单位净值，累计净值，变化
    df,nowtime = obj.get_close()
    if df.empty:
        return HttpResponse(json.dumps({'errCode': 500, 'errMsg': '没有数据！'}, cls=JsonCustomEncoder),'content_type="application/json"')

    macd = wg_macd(df)
    #计算macd
    data[code]['macd'] = macd

    #获取天天基金最新数据
    data[code]['nowtime'] = nowtime

    #基准日
    base_day = sdate
    data[code]['base_day'] = base_day
    #基础净值
    base_data= df.loc[df.index==base_day]
    base_value = base_data['sum_value'].values[0]
    data[c.code]['base_value'] = base_value

    #每次涨跌步长 取5%
    rank_down = round(base_data['net_value'].values[0] * 0.04,2)

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
            points['sdate'] = d
            points['sum_value'] = row['sum_value']
            points['act'] = 'buy'
            points['base'] = row['sum_value']
            points_list.append(points.copy())

        else:
            #不是第一次买入，就开始比较每天的涨跌幅
            chg = row['sum_value'] - points['base']
            #跌
            if chg < 0:
                #跌的多于步长
                if abs(chg) > rank_down:
                    points['sdate'] = d
                    points['sum_value'] = row['sum_value']
                    points['act'] = 'buy'
                    #n个步长
                    n_bc = (points['base'] - row['sum_value']) // rank_down
                    points['base'] = points['base'] - n_bc * rank_down
                    points_list.append(points.copy())
                #跌，但是跌的少
                else:
                    pass
            else:
                if chg > rank_down:
                    points['sdate'] = d
                    points['sum_value'] = row['sum_value']
                    points['act'] = 'sale'
                    n_bc = (row['sum_value'] - points['base']) // rank_down
                    points['base'] = points['base'] +  n_bc * rank_down
                    points_list.append(points.copy())
        #跟踪最近买卖机会
        table_row['chg'] = (df1.loc[df1.index == df1.index.max()]['sum_value'][0] - points['base']) / rank_down*100
        table_row['chg'] = round(table_row['chg'],2)
        table.append(table_row)
        data[c.code]['bs'] = points_list
    #print(json.dumps(points_list, cls=JsonCustomEncoder))
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','data':data,'table':table}, cls=JsonCustomEncoder), 'content_type="application/json"')

def wg_query_table(request):
    table = []
    codes = OuterFundWgConf.objects.all()
    for c in codes:
        info = JqCodeInfo.objects.filter(code=c.code).first()
        temp = {}
        temp['code'] = c.code
        temp['sdate'] = c.sdate
        temp['name'] = info.name
        temp['short_name'] = info.short_name
        table.append(temp)
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','table':table}, cls=JsonCustomEncoder), 'content_type="application/json"')

