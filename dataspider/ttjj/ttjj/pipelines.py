# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ttjj.util import *
from ttjj.models import *

class MysqlStorePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        c = type(item).__name__
        self.obj = type(c+'Model', (Base,), {'__tablename__': c})
        with session_maker() as s:
            #print(item)
            s.merge(self.obj(**item))