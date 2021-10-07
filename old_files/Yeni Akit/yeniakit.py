import json

from scrapy import Spider


def tidy(text):
    tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
                 .replace('\xa0', ' ').strip())
    return tidy_text


with open('yeni_akit_full.json') as json_file:
    news_pages = json.load(json_file)


class SingleSpider(Spider):
    name = 'yeni_akit'
    start_urls = [a.get('Url') for a in news_pages]

    def parse(self, response, **kwargs):
        if '/yazarlar/' in response.request.url:
            text = tidy(''.join(response.css('div.content.forReklamUp p'
                                             ' ::text').getall()))
            if 'fetö' not in text.lower():
                yield {
                    'Url': response.request.url,
                    'empty': True
                }
            else:
                yield {
                    'Url': response.request.url,
                    'Baslik': response.css('h1.title::text').get(),
                    'Tarih': response.css('div.date::text').get(),
                    'Detay': text,
                    'Yazar': response.css('div.author-name::text').get().strip(),
                    'Haber / Kose Yazisi / Konusma': 'Kose Yazisi',
                }
        else:
            text = response.css('div.spot p::text').get() + \
                   ''.join(response.css('div.default-news-content p ::text,h2'
                                        ' ::text').getall())
            if 'fetö' not in text.lower():
                yield {
                    'Url': response.request.url,
                    'empty': True
                }
            else:
                yield {
                    'Url': response.request.url,
                    'Baslik': response.css('h1.title::text').get(),
                    'Tarih': response.css('div.date::text').get()[:10],
                    'Detay': text,
                    'Yazar': '',
                    'Haber / Kose Yazisi / Konusma': 'Haber',
                }
