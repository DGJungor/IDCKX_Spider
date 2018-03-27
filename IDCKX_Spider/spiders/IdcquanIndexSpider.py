import scrapy
from urllib.parse import urljoin

from IDCKX_Spider.items import idcquanindexItem


class IdcquanIndexSpider(scrapy.Spider):
    name = "idcquanindex"
    allowed_domains = ["idcquan.com"]
    start_urls = [
        "http://www.idcquan.com/index/index_1.shtml"
    ]

    def parse(self, response):
        for sel in response.xpath("//div[@class='news_con']/div"):
            # 获取详情页链接
            url = sel.xpath("div[@class='news_nr']/a/@href").extract()

            # 时间
            date = sel.xpath('span/text()').extract()

            # 文章标题
            title = sel.xpath("div[@class='news_nr']/a/span[@class='title']/text()").extract()
            # print('发布日期:%s,标题:%s,链接:%s' % (date, title, url))

            # 以列表页中的标题链接作为 详情页链接  执行 单页爬取的回调函数
            yield scrapy.Request(url[0], callback=self.parse_dir_contents, dont_filter=True)

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
        for con in response.xpath("//div[@class='newsbox inner']"):
            item = idcquanindexItem()

            # 标题
            item['title'] = con.xpath(
                "div[@class='article_detail article-infos']/div[@class='title']/text()").extract_first()

            # 内容
            item['content'] = \
                con.xpath("//div[@class='clear deatil article-content fontSizeSmall BSHARE_POP']").extract()[0].replace(
                    '\r', '').replace('\n', '').replace('\t', '')

            # print(item)

            yield item
