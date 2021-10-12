import json
import requests

from scrapy import Spider


def tidy(text):
    tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
                 .replace('\xa0', ' ').strip())
    return tidy_text


with open('haberturk_links.json') as json_file:
    all_pages = json.load(json_file)

all_urls = [a.get('link') for a in all_pages]
last_index = all_urls.index('https://www.haberturk.com/japonya-kuzey-kore-nin-'
                            'balistik-fuze-denedigini-acikladi-3204342')


class AllSpider(Spider):
    name = 'haberturk_all'
    start_urls = all_urls[last_index + 1:]

    def parse(self, response, **kwargs):
        if 'fetö' in response.text.lower():
            yield {
                'link': response.url
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
