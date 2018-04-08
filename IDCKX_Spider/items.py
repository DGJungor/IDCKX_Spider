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


class idcquanItem(scrapy.Item):
	# 文章识别码   一般为  主域+下划线+文章ID  例: idcquan.com_9527
	dis_id = scrapy.Field()

	# 文章链接
	url = scrapy.Field()

	# 文章标题
	title = scrapy.Field()

	# 文章分类
	category = scrapy.Field()

	# 文章来源
	source = scrapy.Field()

	# 文章日期
	date = scrapy.Field()

	# 关键词
	keywords = scrapy.Field()

	# 文章描述
	description = scrapy.Field()

	# 文章内容
	content = scrapy.Field()

	# 缩略图
	thumbnail = scrapy.Field()

	# 更多信息
	more = scrapy.Field()

	# 爬虫添加时间
	create_time = scrapy.Field()
