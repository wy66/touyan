# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TtjjCode(scrapy.Item):
    # define the fields for your item here like:
    jjcode = scrapy.Field()
    fname = scrapy.Field()
    sname = scrapy.Field()
    stype = scrapy.Field()
    sday = scrapy.Field()
    gm = scrapy.Field()

class TtjjNet(scrapy.Item):
    # define the fields for your item here like:
    datadate = scrapy.Field()
    jjcode = scrapy.Field()
    net_value = scrapy.Field()
    sum_value = scrapy.Field()

class TtjjTop10Stock(scrapy.Item):
    # define the fields for your item here like:
    datadate = scrapy.Field()
    jjcode = scrapy.Field()
    scode = scrapy.Field()
    sname = scrapy.Field()
    pct = scrapy.Field()
    num = scrapy.Field()