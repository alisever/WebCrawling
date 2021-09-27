import scrapy
import datetime
from json import load


base = 'https://www.posta.com.tr/arama?q=fet%C3%B6&isinfinity=true&page={}'


class AllSpider(scrapy.Spider):
    name = 'posta_all'
    page_no = 0
    start_urls = [base.format(page_no)]

    def parse(self, response, **kwargs):
        for news in response.css('a.search-results__item'):
            yield {
                'link': 'https://www.posta.com.tr' +
                        news.css('::attr(href)').get()
            }
        if self.page_no < 221:
            self.page_no += 1
            yield scrapy.Request(base.format(self.page_no))


with open('posta.json') as json_file:
    news_pages = load(json_file)


class SingleSpider(scrapy.Spider):
    name = 'posta'
    start_urls = [a.get('link') for a in news_pages]

    def parse(self, response, **kwargs):
        if '/yazarlar/' in response.request.url:
            yield {
                'Url': response.request.url,
                'Baslik': (response.css('h1.author-column__header__title::'
                           'text').get().replace('\r', '').replace('\n', '').
                           replace('\t', '')),
                'Tarih': (response.css('div.author-column__date > time::text').
                          get().replace('\r', '').replace('\n', '').
                          replace('\t', '').partition(',')[0]),
                'Detay': (''.join(response.css('div.author-column__content '
                          'p ::text').getall()).replace("\r", "").
                          replace("\n", "").replace("\t", "").
                          replace("\xa0", " ").strip()),
                'Yazar': response.css('a.author-info__name::text').get(),
                'Haber / Kose Yazisi / Konusma': 'Kose Yazisi'
            }
        else:
            yield {
                'Url': response.request.url,
                'Baslik': (response.css('h1.news-detail__info__title::text').
                           get().replace('\r', '').replace('\n', '').
                           replace('\t', '')),
                'Tarih': (response.css('span.news-detail__info__date__item::'
                          'text').get().replace('\r', '').replace('\n', '').
                          replace('\t', '').partition(',')[0]),
                'Detay': (''.join(response.css('div.news-detail__body__content'
                          '.clearfix > p ::text').getall()).replace("\r", "").
                          replace("\n", "").replace("\t", "").
                          replace("\xa0", " ").strip()),
                'Yazar': '',
                'Haber / Kose Yazisi / Konusma': 'Haber'
            }


class ExceptionSpider(scrapy.Spider):
    name = 'posta_except'
    start_urls = ['https://www.yenisafak.com/dusunce-gunlugu/'
                  '15-temmuz-2016da-turkiyede-ne-oldu-2499421']

    def parse(self, response, **kwargs):
        yield {
                'Url': response.request.url,
                'Baslik': response.css('h1.title::text').get(),
                'Tarih': response.css('time.item.time::text').get().partition(
                    ',')[0],
                'Detay': ''.join(response.css('[class^="text text"]::text'
                                              ).getall()).strip(),
                'Yazar': response.css('div.text.text-666666 > strong::text').get()[1:],
                'Haber / Kose Yazisi / Konusma': 'Kose Yazisi'
            }