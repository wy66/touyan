#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/7 14:33
# @Author  : wangyang
# @File    : run.py
# @Software: PyCharm
from scrapy import cmdline
cmdline.execute('scrapy crawl ttjj_net'.split(' '))