import json
import requests

from scrapy import Spider


def tidy(text):
    if text is None:
        return ''
    tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
                 .replace('\xa0', ' ').strip())
    return tidy_text


with open('haberturk_links.json') as json_file:
    all_pages = json.load(json_file)

all_urls = [a.get('link') for a in all_pages]
last_index = all_urls.index('https://www.haberturk.com/htyazar/ayse-ozek-karasu/33')


class AllSpider(Spider):
    name = 'haberturk_all'
    start_urls = all_urls[last_index + 1:]

    def parse(self, response, **kwargs):
        if 'fetö' in response.text.lower():
            yield {
                'link': response.url
            }


with open('haberturk5.json') as json_file:
    news_pages = json.load(json_file)


class SingleSpider(Spider):
    name = 'haberturk'
    start_urls = [a.get('link') for a in news_pages]

    def parse(self, response, **kwargs):
        if '/yazarlar/' in response.url:
            tur = 'Kose Yazisi'
            yazar = tidy(response.css('span.name::text').get())
        else:
            tur = 'Haber'
            yazar = ''
        text = tidy(response.css('h2.spot-title::text').get())
        for item in response.css('article.content.type1 > p ::text').getall():
            text += tidy(item)
        all_text = response.css('h1.title::text').get() + tidy(text)
        if 'fetö' not in all_text.lower():
            return
        yield {
            'Url': response.request.url,
            'Baslik': response.css('h1.title::text').get(),
            'Tarih': response.css('span.date time::text').get(),
            'Detay': tidy(text),
            'Yazar': yazar,
            'Haber / Kose Yazisi / Konusma': tur,
        }

# scrapy crawl haberturk -O haberturk6.json --logfile spider.log --loglevel ERROR
