# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


__author__ = ' ZhangJun 568171152@qq.com'

import json
import codecs


# 以Json的形式存储
class IdckxSpiderJsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('Idckx.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class IdckxSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
