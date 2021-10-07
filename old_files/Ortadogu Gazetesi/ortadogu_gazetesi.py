import scrapy
from json import load

base = 'https://www.haberturk.com/arama/?tr=fet%C3%B6&siralama=yeni'


class AllSpider(scrapy.Spider):
    name = 'ortadogu_gazetesi_all'
    start_urls = [base.format(1)]
    page_no = 1

    def parse(self, response, **kwargs):
        for news in response.css('div.thumbnail.thumbnail-radius'):
            yield {
                'link': news.css('a').attrib['href']
            }

        if self.page_no < 30:
            self.page_no += 1
            url = base.format(self.page_no)
            yield scrapy.Request(url)


with open("ortadogugazetesi.json") as json_file:
    news_pages = load(json_file)


class SingleSpider(scrapy.Spider):
    name = 'ortadogu_gazetesi_single'
    start_urls = [a.get('link') for a in news_pages]

    def parse(self, response, **kwargs):
        try:
            yazar = response.css('ul.list-inline.mb-0').css('li')[2].css(
                'span').css('a::text').get()
        except IndexError:
            yazar = ''
        try:
            tarih = response.css('ul.list-inline.mb-0').css('li')[1].css(
                'span::text').get()
        except IndexError:
            tarih = response.css('ul.list-inline').css('li')[1].css(
                'span::text').get()
        yield {
            'Url': response.request.url,
            'Baslik': response.css('div.panel-title > h1.font-bold::text'
                                   ).get(),
            'Tarih': tarih,
            'Detay': (''.join(response.css('div.text > p ::text').getall()).
                      replace("\r", "").replace("\n", "").replace("\xa0", " ")
                      ),
            'Yazar': yazar,
            'Haber / Kose Yazisi / Konusma': 'Haber'
        }
