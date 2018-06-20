import pymysql  # 数据库操作库
import scrapy
import time
from urllib.parse import urljoin
from IDCKX_Spider.items import idcquanItem
from scrapy.utils.project import get_project_settings  # 导入seetings配置
from scrapy.utils.response import get_base_url  # 获取链接模块
from tld import get_tld  # 获取文章主域的模块


class idcquanSpider(scrapy.Spider):
    name = "idcquan"
    allowed_domains = ["idcquan.com"]
    start_urls = [
        # "http://www.idcquan.com/index/index_1.shtml",
        "http://www.idcquan.com/index/index_20.shtml",
        # "http://www.idcquan.com/index/index_1.shtml",
        # 'http://news.idcquan.com/index6_1.shtml',
        # "http://www.idcquan.com/cloud/index6_1.shtml"
    ]

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )

        # 查询数据库中最后一篇文章的时间
        self.post_latest = self.query_post_latest(dbparams)

        # print('==============================================================')
        # print (post_lates)
        # print('%s' % (ttt))
        # print('%s' % (dbparams['host']))
        # print('==============================================================')

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

        # 获取上一页链接
        next_pages = response.xpath("//a[@class='prev']/@href").extract()

        # 获取下一页链接
        # next_pages = response.xpath("//a[@class='next']/@href").extract()

        # 判断有无下一页  有则执行回调函数
        if next_pages:
            # 对分页链接重新组合
            # next_page = urljoin(SITE_URL, next_pages[0].extract())

            # 以 下一页链接为回调函数参数  重新执行爬取列表页数据
            yield scrapy.Request(next_pages[0], callback=self.parse, dont_filter=True)

    # 对单页详情页 进行数据爬取
    def parse_dir_contents(self, response):

        # 实例化
        item = idcquanItem()
        for con in response.xpath("//div[@class='newsbox inner']"):
            # 文章所属主域
            item['host'] = get_tld(get_base_url(response))

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
            # 如果内容为空则添加来源文字为位置来源
            if item['source'] == '':
                item['source'] = con.xpath(
                    "div[@class='article_detail article-infos']/div[@class='authorbox clearfix']/div[@class='source']/a/text()").extract_first().replace(
                    '\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('来源：', '')
                if item['source'] == '':
                    item['source'] = '未知'

            # 内容
            item['content'] = \
                con.xpath("//div[@class='clear deatil article-content fontSizeSmall BSHARE_POP']").extract()[
                    0].replace(
                    '\r', '').replace('\n', '').replace('\t', '').replace(
                    ' class="clear deatil article-content fontSizeSmall BSHARE_POP"', '')

            # 日期时间
            # item['date'] = time.mktime(response.meta['date'][0])
            item['date'] = response.meta['date'][0]

            # 转时间戳
            timeArray = time.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
            item['date'] = int(time.mktime(timeArray))

            # 分类
            item['category'] = response.meta['category'][0]

            # 缩略图
            item['thumbnail'] = response.meta['thumbnail'][0]

            # 文章链接
            item['url'] = response.meta['url'][0]

        # print(item['date'])
        if item['date'] > self.post_latest:
            yield item
        else:
            print('文章不符合入库标准')
            print(item['date'])
            print(self.post_latest)

    # 根据数据库文章时间数据数据检查重复
    def check_repetition(self):
        pass

    # 查询数据库中最新文章时间
    def query_post_latest(self, dbparams):
        conn = pymysql.connect(host=dbparams['host'], port=3306, user=dbparams['user'], passwd=dbparams['passwd'],
                               db=dbparams['db'], charset=dbparams['charset'])

        cursor = conn.cursor()
        cursor.execute(
            "SELECT idckx_spider_post.date FROM idckx_spider_post WHERE idckx_spider_post.`host`='idcquan.com' ORDER BY date DESC")

        # 获取剩余结果的第一行数据
        latest_date = cursor.fetchone()

        # 关闭数据库
        cursor.close()
        conn.close()
        return latest_date[0]
