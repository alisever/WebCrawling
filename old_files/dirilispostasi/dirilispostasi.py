import json
import random

from scrapy import Spider, Request


def tidy(text):
    tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
                 .replace('\xa0', ' ').strip())
    return tidy_text


base = 'https://www.dirilispostasi.com/ara?key=fet%C3%B6&page={}'

with open('agents.txt', 'r') as f:
    agents = [line.rstrip() for line in f.readlines()]


class AllSpider(Spider):
    name = 'dirilis_all'

    start_urls = [base.format(i) for i in range(1, 752)]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, headers={'User-agent': random.choice(agents)}, dont_filter=True)

    def parse(self, response, **kwargs):
        print(response.status)
        for link in response.css('h3.b > a::attr(href)').getall():
            yield {
                'link': link
            }


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
