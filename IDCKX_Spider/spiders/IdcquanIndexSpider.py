import scrapy
from urllib.parse import urljoin

from IDCKX_Spider.items import idcquanindexItem


class IdcquanIndexSpider(scrapy.Spider):
    name = "idcquanindex"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.idcquan.com/index/index_1.shtml"
    ]

    def parse(self, response):
        for sel in response.xpath("//div[@class='news_con']/div"):
            # 获取详情页链接
            url = sel.xpath("div[@class='news_nr']/a/@href").extract()
            date = sel.xpath('span/text()').extract()
            title = sel.xpath("div[@class='news_nr']/a/span[@class='title']/text()").extract()
            # print('发布日期:%s,标题:%s,链接:%s' % (date, title, url))
            yield scrapy.Request(url[0], callback=self.parse_dir_contents, dont_filter=True)

        next_pages = response.xpath("//a[@class='next']/@href").extract()

        if next_pages:
            # next_page = urljoin(SITE_URL, next_pages[0].extract())
            yield scrapy.Request(next_pages[0], callback=self.parse, dont_filter=True)

        # print('链接:%s' % (next_pages))

    # 对单页详情页 进行数据爬取
    def parse_dir_contents(self, response):
        for con in response.xpath("//div[@class='newsbox inner']"):
            item = idcquanindexItem()
            item['title'] = con.xpath("div[@class='article_detail article-infos']/div[@class='title']/text()").extract()

            # item['link'] = sel.xpath('a/@href').extract()
            # item['desc'] = sel.xpath('text()').extract()
            # print(item['title'])
            yield item
