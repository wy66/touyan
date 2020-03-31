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
    for c in codes:
        obj = GetFundCloseJq(c.code,sdate='2018-01-01')
        obj.get_close()
    return HttpResponse(json.dumps({'errCode':200,'errMsg':'success'}, cls=JsonCustomEncoder), 'content_type="application/json"')


