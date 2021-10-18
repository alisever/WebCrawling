import json

import scrapy
from scrapy import Spider


def tidy(text):
    tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
                 .replace('\xa0', ' ').strip())
    return tidy_text


base = 'https://odatv4.com/haber-sayfa?query=fet%C3%B6&page={}'


class AllSpider(Spider):
    name = 'odatv_all'
    page_no = 1
    start_urls = [base.format(page_no)]

    def parse(self, response, **kwargs):
        if not response.css('a.news-item-link.br5::attr(href)').getall():
            return
        for link in response.css('a.news-item-link.br5::attr(href)').getall():
            yield {
                'link': response.urljoin(link)
            }
        self.page_no += 1
        yield scrapy.Request(base.format(self.page_no))
#
#
# with open('') as json_file:
#     news_pages = json.load(json_file)
#
#
# class SingleSpider(Spider):
#     name = 'template2'
#     start_urls = [a.get('link') for a in news_pages]
#
#     def parse(self, response, **kwargs):
#         yield {
#             'Url': response.request.url,
#             'Baslik': tidy(''),
#             'Tarih': tidy(''),
#             'Detay': tidy(''),
#             'Yazar': tidy(''),
#             'Haber / Kose Yazisi / Konusma': '',
#         }
#
# # scrapy crawl template2 -O template.json --logfile spider.log --loglevel ERROR
