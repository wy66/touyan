#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 9:08
# @Author  : wangyang
# @File    : urls.py
# @Software: PyCharm


from django.conf.urls import url, include
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^fund_general$', TemplateView.as_view(template_name='fund_general.html')),

    url(r'^wg$', TemplateView.as_view(template_name='wg.html')),
    url(r'^jj_codes$', jj_codes),
    url(r'^wg_add$', wg_add),
    url(r'^wg_query$', wg_query),
    url(r'^wg_query_table$', wg_query_table),

    url(r'^dl$', TemplateView.as_view(template_name='dl.html')),
    url(r'^dl_query$', dl_query),
    url(r'^fund_general_query$', fund_general_query),
]

