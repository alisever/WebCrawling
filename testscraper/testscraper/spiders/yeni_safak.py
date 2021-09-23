import scrapy
import datetime
from json import load


base = 'https://www.yenisafak.com/arama/fet%C3%B6?word=fet%C3%B6&page={}&' \
       'start={}&end={}'


class AllSpider(scrapy.Spider):
    name = 'yeni_safak_all'
    page_no = 0
    end_date = datetime.date.today()
    start_urls = [base.format(page_no, (end_date - datetime.timedelta(days=30))
                              .strftime("%d.%m.%Y"),
                              end_date.strftime("%d.%m.%Y"))]

    def parse(self, response, **kwargs):
        if response.css('div.notfound'):
            self.page_no = 0
            self.end_date = self.end_date - datetime.timedelta(days=30)

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
            self.page_no += 1

        url = base.format(self.page_no, (self.end_date - datetime.
                          timedelta(days=30)).strftime("%d.%m.%Y"),
                          self.end_date.strftime("%d.%m.%Y"))
        yield scrapy.Request(url)


with open('yenisafakhaberleri.json') as json_file:
    news_pages = load(json_file)


# class SingleSpider(scrapy.Spider):
#     name = 'yeni_safak'
#     start_urls = [a.get('link') for a in news_pages]
#
#     def parse(self, response, **kwargs):
#         try:
#             yazar = response.css('ul.list-inline.mb-0').css('li')[2].css(
#                 'span').css('a::text').get()
#         except IndexError:
#             yazar = ''
#         try:
#             tarih = response.css('ul.list-inline.mb-0').css('li')[1].css(
#                 'span::text').get()
#         except IndexError:
#             tarih = response.css('ul.list-inline').css('li')[1].css(
#                 'span::text').get()
#         yield {
#             'Url': response.request.url,
#             'Baslik': response.css('div.panel-title > h1.font-bold::text'
#                                    ).get(),
#             'Tarih': tarih,
#             'Detay': (''.join(response.css('div.text > p ::text').getall()).
#                       replace("\r", "").replace("\n", "").replace("\xa0", " ")
#                       ),
#             'Yazar': yazar,
#             'Haber / Kose Yazisi / Konusma': 'Haber'
#         }
