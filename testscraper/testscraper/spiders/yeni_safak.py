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


with open('yenisafak_1.json') as json_file:
    news_pages = load(json_file)


class SingleSpider(scrapy.Spider):
    name = 'yeni_safak'
    start_urls = [a.get('link') for a in news_pages]

    def parse(self, response, **kwargs):
        if '/foto-galeri' in response.request.url:
            return
        elif '/video-galeri' in response.request.url:
            return
        elif '/infografik' in response.request.url:
            return
        text = ''.join(response.css('[class^="text text"]::text'
                                    ).getall()).strip()
        if text == '':
            text = ''.join(response.css('[class^="text  text"]::text'
                                        ).getall()).strip()
        if text == '':
            text = ''.join(response.css('p.non-card ::text').getall())
        if text == '':
            text = ''.join(response.css(
                '[class^="text text"] > p ::text').getall())
        if '/yazarlar/' in response.request.url:
            yield {
                'Url': response.request.url,
                'Baslik': response.css('div.title > h1::text').get(),
                'Tarih': response.css('time.item.time::text').get().partition(
                    ',')[0],
                'Detay': text.replace("\r", "").replace("\n", "").replace(
                    "\xa0", " "),
                'Yazar': ''.join(response.css('div.author-bio div.name ::text'
                                              ).getall()).strip(),
                'Haber / Kose Yazisi / Konusma': 'Kose Yazisi'
            }
        else:
            try:
                response.css('time.item.time::text').get().partition(',')[0]
            except AttributeError:
                referer_url = response.request.meta['redirect_urls']
                print(referer_url, 'failed')
                return
            yield {
                'Url': response.request.url,
                'Baslik': response.css('h1.title::text').get(),
                'Tarih': response.css('time.item.time::text').get().partition(
                    ',')[0],
                'Detay': text.replace("\r", "").replace("\n", "").replace(
                    "\xa0", " "),
                'Yazar': response.css('strong.name::text').get(),
                'Haber / Kose Yazisi / Konusma': 'Haber'
            }


class ExceptionSpider(scrapy.Spider):
    name = 'yeni_safak_except'
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