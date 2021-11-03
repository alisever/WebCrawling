import scrapy
from pandas import read_csv
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule, SitemapSpider

from ..items import AllUrlsItem


class SozcuSitemapSpider(SitemapSpider):
    name = 'sozcu_sitemap'
    allowed_domains = ['sozcu.com.tr']
    sitemap_urls = ['https://www.sozcu.com.tr/robots.txt']

    def parse(self, response, **kwargs):
        yield {'url': response.url}

# scrapy crawl sozcu_sitemap -O sozcu_sitemap.json --logfile spider.log --loglevel ERROR


class SozcuSpider(CrawlSpider):
    name = 'sozcu'
    allowed_domains = ['sozcu.com.tr']
    start_urls = ['https://www.sozcu.com.tr/']

    data = read_csv('sozcu_sitemap.csv')
    start_urls += data['url'].tolist()

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    keyword = 'feto'

    def parse_item(self, response):
        l = ItemLoader(item=AllUrlsItem(), response=response)
        l.add_value('url', response.url)
        if self.keyword in response.text.lower().encode('utf-8').decode():
            l.add_value('keyword', 1)
        else:
            l.add_value('keyword', 0)
        return l.load_item()

# scrapy crawl sozcu --logfile spider.log --loglevel ERROR -s JOBDIR=crawls/SozcuSpider
