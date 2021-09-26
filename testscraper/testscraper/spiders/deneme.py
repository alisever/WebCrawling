import scrapy
import datetime
from json import load


base = 'https://www.dirilispostasi.com/haber/7808794/f' \
       'etonun-emniyet-yapilanmasina-darbe-6-kisiye-gozalti'


class AllSpider(scrapy.Spider):
    name = 'deneme'

    start_urls = [base]

    def parse(self, response, **kwargs):
        if response.css('div.notfound'):
            pass
        else:
            for news in response.css('div.search-result-list').css('a.entry'):
                if news.css('div.category > span::text').get():
                    news_type = 'Haber'
                else:
                    news_type = 'Kose Yazisi'
                yield {
                    'link': news.css('a.entry').attrib['href'],
                    'type': news_type
                }
