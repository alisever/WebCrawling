import json

from scrapy import Spider, Request


def tidy(text):
    tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
                 .replace('\xa0', ' ').replace('\ufffd', '').strip())
    return tidy_text


base = 'https://www.milliyet.com.tr/api/search/searchcontentloadmore?' \
       'query=feto&page={}&isFromNewsSearchPage=true'


class AllSpider(Spider):
    name = 'milliyet_all'
    page_no = 346
    start_urls = [base.format(page_no)]

    def parse(self, response, **kwargs):
        for link in response.css('div.news__item.col-md-12.col-sm-6 a.news__titles-link::attr(href)').getall():
            yield {
                'link': 'https://www.milliyet.com.tr' + link
            }
        self.page_no += 1
        if self.page_no < 402:
            yield Request(base.format(self.page_no), callback=self.parse)


with open('milliyet3.json') as json_file:
    news_pages = json.load(json_file)


class SingleSpider(Spider):
    name = 'milliyet'
    start_urls = [a.get('link') for a in news_pages]

    def parse(self, response, **kwargs):
        if '/galeri/' in response.url:
            return
        if '/milliyet-tv/' in response.url:
            return
        if '/skorer-tv/' in response.url:
            return
        text = ''.join(response.css('h2.nd-article__spot ::text').getall()) + \
               ''.join(response.css('div.nd-content-column p ::text').getall())
        yield {
            'Url': response.request.url,
            'Baslik': response.css('h1.nd-article__title::text').get(),
            'Tarih': response.css('div.nd-article__info-block::text').get()[:10],
            'Detay': tidy(text),
            'Yazar': '',
            'Haber / Kose Yazisi / Konusma': 'Haber',
        }


class ExceptionSpider(Spider):
    name = 'milliyet_except'
    page_no = 346
    start_urls = ['https://www.milliyet.com.tr/ekonomi/son-dakika-otobus-biletlerine-tavan-ucret-uygulamasi-getirildi-6552926',
                  'https://www.milliyet.com.tr/gundem/diyanet-hutbe-9-temmuz-cuma-hutbesi-konusu-6548795',
                  'https://www.milliyet.com.tr/gundem/16-temmuz-tatil-mi-bu-yil-16-temmuz-resmi-tatil-mi-idari-izin-sayilacak-mi-6554087']

    def parse(self, response, **kwargs):
        text = ''.join(response.css('h2.rhd-article-spot ::text').getall()) + \
               ''.join(response.css('h3.description ::text, h2.title ::text').getall())
        yield {
            'Url': response.request.url,
            'Baslik': response.css('h1.rhd-article-title::text').get(),
            'Tarih': response.css('span.rhd-time-box-text.rgc_date::text').get()[4:18],
            'Detay': tidy(text),
            'Yazar': '',
            'Haber / Kose Yazisi / Konusma': 'Haber',
        }
