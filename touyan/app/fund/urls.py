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
    url(r'^wg$', TemplateView.as_view(template_name='wg.html')),
    url(r'^wg_add$', wg_add),
    url(r'^wg_query$', wg_query),
]

