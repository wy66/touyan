from django.shortcuts import render,HttpResponse
from django.db import connections
from django.forms.models import model_to_dict
from django.db import connections
from .models import *
import json
import decimal
import pandas as pd
import numpy as np
from .datas.fund import *
from .call import  *
# Create your views here.



#网格策略步长
GLOBAL_BC = 0.04

class JsonCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, pd.datetime):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return super(JsonCustomEncoder, self).default(obj)

def jj_codes(request):
    objs = jjCode.objects.all().order_by('jjcode')
    data = [model_to_dict(x) for x in objs]
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','data':data}, cls=JsonCustomEncoder), 'content_type="application/json"')


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

def aa(x):
    if np.isnan(x):
        return ''
    elif x > 0:
        return 1
    else:
        return -1

def wg_query(request):
    global GLOBAL_BC
    code = request.POST.get('code')
    sdate = request.POST.get('sdate')
    name = request.POST.get('name')
    data = {}
    obj = GetFundClose(code,sdate='2018-01-01')

    #获取基金单位净值，累计净值，变化
    df,nowtime = obj.get_close()
    if df.empty:
        return HttpResponse(json.dumps({'errCode': 500, 'errMsg': '没有数据！'}, cls=JsonCustomEncoder),'content_type="application/json"')

    macd = wg_macd(df)
    #计算macd
    data['macd'] = macd

    #获取天天基金最新数据
    data['nowtime'] = nowtime

    #基准日
    base_day = sdate
    base_day = datetime.date(int(base_day[:4]),int(base_day[5:7]),int(base_day[8:]))
    data['base_day'] = base_day
    #基础净值
    if df.index.min() > base_day:
        base_day = df.index.min()
    base_data= df.loc[df.index==base_day]
    base_value = base_data['sum_value'].values[0]
    data['base_value'] = base_value

    #每次涨跌步长 取5%
    rank_down = round(base_data['net_value'].values[0] * GLOBAL_BC,2)

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
    data['markline'] = markline
    data['name'] = name
    data['data'] = df.reset_index().fillna('').to_dict(orient='list')

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
        # table_row['chg'] = (df1.loc[df1.index == df1.index.max()]['sum_value'][0] - points['base']) / rank_down*100
        # table_row['chg'] = round(table_row['chg'],2)
        # table.append(table_row)
        data['bs'] = points_list
    #print(json.dumps(points_list, cls=JsonCustomEncoder))
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','data':data}, cls=JsonCustomEncoder), 'content_type="application/json"')

def wg_query_table(request):
    table = []
    codes = OuterFundWgConf.objects.all()
    for c in codes:
        info = jjCode.objects.filter(jjcode=c.code).first()
        temp = {}
        temp['code'] = c.code
        temp['sdate'] = c.sdate
        temp['name'] = info.fname
        temp['short_name'] = info.sname

        obj = GetFundClose(c.code, sdate='2018-01-01')

        # 获取基金单位净值，累计净值，变化
        df, nowtime = obj.get_close()
        if df.empty:
            continue
        temp['nowtime'] = nowtime
        base_day = c.sdate
        df1 = df.loc[df.index >= base_day]
        # 每次涨跌步长 取5%
        # 基础净值
        if df1.index.min() > base_day:
            base_day = df1.index.min()
        base_data = df1.loc[df1.index == base_day]

        rank_down = round(base_data['net_value'].values[0] * GLOBAL_BC, 2)
        points = {}
        for d, row in df1.iterrows():
            # 初始，第一天买入
            if not points:
                points['sdate'] = d
                points['sum_value'] = row['sum_value']
                points['act'] = 'buy'
                points['base'] = row['sum_value']

            else:
                # 不是第一次买入，就开始比较每天的涨跌幅
                chg = row['sum_value'] - points['base']
                # 跌
                if chg < 0:
                    # 跌的多于步长
                    if abs(chg) > rank_down:
                        points['sdate'] = d
                        points['sum_value'] = row['sum_value']
                        points['act'] = 'buy'
                        # n个步长
                        n_bc = (points['base'] - row['sum_value']) // rank_down
                        points['base'] = points['base'] - n_bc * rank_down
                    # 跌，但是跌的少
                    else:
                        pass
                else:
                    if chg > rank_down:
                        points['sdate'] = d
                        points['sum_value'] = row['sum_value']
                        points['act'] = 'sale'
                        n_bc = (row['sum_value'] - points['base']) // rank_down
                        points['base'] = points['base'] + n_bc * rank_down
        chg = (df1.loc[df1.index == df1.index.max()]['sum_value'][0] - points['base']) / rank_down * 100.0
        chg = round(chg,2)
        temp['chg'] = chg
        if chg >99:
            send_email(info.name+'卖点出现!','')
        elif chg < -99:
            send_email(info.name + '买点出现!', '')
        table.append(temp)

    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','table':table}, cls=JsonCustomEncoder), 'content_type="application/json"')

def dl_query(request):
    codes = {
        '481012':'深红利联接A',
        '005064':'广发中证全指家用电器指数C',
        '000248':'汇添富消费联接',
        '161725':'白酒分级'
    }
    df_all = None
    #N日涨跌幅
    N = 13
    #M日均线
    M = 13
    for c in codes:
        obj = GetFundClose(c, sdate='2018-01-01')

        # 获取基金单位净值，累计净值，变化
        df, nowtime = obj.get_close()
        df['N'] = df['sum_value'].shift(N)
        df['M'] = df['sum_value'].rolling(M).mean()
        df['last'] = df['sum_value'].shift(1)
        df['chg'] = (df['sum_value'] - df['last']) / df['last']
        df = df.dropna(subset=['N','M'])
        df = df.rename(columns={'net_value':c+'_net','sum_value':c+'_sum','N':c+'_N','M':c+'_M','chg':c+'_chg'})
        if df_all is None:
            df_all = df
        else:
            df_all = df_all.join(df)
    df_all = df_all.sort_index()


    for d,row in df_all.iterrows():
        zdf = {}
        for c in codes:
            zdf[c] = (row[c+'_sum'] - row[c+'_N']) /  row[c+'_N']
        max_code = [x for x in zdf if zdf[x] == max(zdf.values())][0]
        if row[max_code] > row[max_code+'_M']:
            print(d,max_code)

    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','table':{}}, cls=JsonCustomEncoder), 'content_type="application/json"')

def fund_general_query(request):
    sql = '''
        select datadate,jjcode,net_value from ttjjnet where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(datadate)  
    '''
    df = pd.read_sql(sql,connections['default'])
    df.pivot(index='datadate', columns='jjcode',values='net_value')
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success','table':{}}, cls=JsonCustomEncoder), 'content_type="application/json"')


