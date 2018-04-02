import scrapy
from urllib.parse import urljoin

from IDCKX_Spider.items import idcquanindexItem


class IdcquanIndexSpider(scrapy.Spider):
	name = "idcquanindex"
	allowed_domains = ["idcquan.com"]
	start_urls = [
		# "http://www.idcquan.com/index/index_1.shtml",
		"http://www.idcquan.com/cloud/index6_1.shtml"
	]

	def parse(self, response):
		for sel in response.xpath("//div[@class='news_con']/div"):
			# 文章标题
			title = sel.xpath("div[@class='news_nr']/a/span[@class='title']/text()").extract()

			# 获取详情页链接
			url = sel.xpath("div[@class='news_nr']/a/@href").extract()

			# 时间
			date = sel.xpath('span/text()').extract()

			# thumbnail  缩略图
			thumbnail = sel.xpath('a/img/@src').extract()

			# 分类 category
			category = sel.xpath("div[@class='news_nr']/a/span[@class='tip']/text()").extract()

			# 以列表页中的标题链接作为 详情页链接  执行 单页爬取的回调函数
			# yield scrapy.Request(url[0], callback=self.parse_dir_contents, dont_filter=True)
			res = scrapy.Request(url[0], callback=self.parse_dir_contents, dont_filter=True)

			# 传参 时间
			res.meta['date'] = date

			# 传参 缩略图
			res.meta['thumbnail'] = thumbnail

			# 传参 文章链接
			res.meta['url'] = url

			# 传参 分类
			res.meta['category'] = category

			yield res

		# 获取下一页链接
		next_pages = response.xpath("//a[@class='next']/@href").extract()

		# 判断有无下一页  有则执行回调函数
		if next_pages:
			# 对分页链接重新组合
			# next_page = urljoin(SITE_URL, next_pages[0].extract())

			# 以 下一页链接为回调函数参数  重新执行爬取列表页数据
			yield scrapy.Request(next_pages[0], callback=self.parse, dont_filter=True)

	# 对单页详情页 进行数据爬取
	def parse_dir_contents(self, response):
		# 实例化

		item = idcquanindexItem()
		for con in response.xpath("//div[@class='newsbox inner']"):
			# 标题
			item['title'] = con.xpath(
				"div[@class='article_detail article-infos']/div[@class='title']/text()").extract_first().replace(
				'\r', '').replace('\n', '').replace('\t', '').replace('<br>', '').replace(' ', '')

			# 关键词 keywords
			item['keywords'] = con.xpath("//meta[@name='keywords']/@content").extract_first().replace(' ', ',')

			# 描述 description
			item['description'] = con.xpath("//meta[@name='description']/@content").extract_first()

			# 来源
			item['source'] = con.xpath(
				"div[@class='article_detail article-infos']/div[@class='authorbox clearfix']/div[@class='source']/text()").extract_first().replace(
				'\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('来源：', '')

			# 内容
			item['content'] = \
				con.xpath("//div[@class='clear deatil article-content fontSizeSmall BSHARE_POP']").extract()[
					0].replace(
					'\r', '').replace('\n', '').replace('\t', '').replace(
					' class="clear deatil article-content fontSizeSmall BSHARE_POP"', '')

			# 日期时间
			item['date'] = response.meta['date'][0]

			# 分类
			item['category'] = response.meta['category'][0]

			# 缩略图
			item['thumbnail'] = response.meta['thumbnail'][0]

			# 文章链接
			item['url'] = response.meta['url'][0]

		# print(item['url'])

		yield item
