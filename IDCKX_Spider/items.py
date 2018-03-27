# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IdckxSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class idcquanindexItem(scrapy.Item):
    # item['title'] = scrapy.Field()
    # item = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
