import re

import scrapy
from scrapy import Spider


def tidy(text):
    tidy_text = (text.replace('\r', '').replace('\n', ' ').replace('\t', '')
                 .replace('\xa0', ' ').strip())
    return tidy_text


base = 'https://www.tbmm.gov.tr/Tutanaklar/Birlesimler?' \
       'donemKodu={}&yasamaYili={}'

all_pages = [(24, 4), (24, 5), (25, 1), (25, 2), (26, 1), (26, 2), (26, 3),
             (27, 1), (27, 2), (27, 3), (27, 4), (27, 5)]


class SingleSpider(Spider):
    name = 'tbmm'
    start_urls = [base.format(i, j) for i, j in all_pages]
    # start_urls = ['https://www.tbmm.gov.tr/Tutanaklar/Tutanak?BirlesimSiraNo=22195&BaslangicSayfa=1&BitisSayfa=1&Tur=H']

    def parse(self, response, **kwargs):
        for page in response.css('div[id=main-area] > div > a::attr(href)'
                                 ).getall():
            yield scrapy.Request(response.urljoin(page),
                                 callback=self.join_pages,
                                 )
        # yield scrapy.Request(response.url, callback=self.join_pages)

    def join_pages(self, response):
        page_count = response.css('div[id=main-area] div span ::text').getall(
                     )[1].strip().split()[2]
        if page_count in ['0', '1']:
            heading = [a.strip() for a in
                       response.css('span.main-area-title::text').getall()]
            heading = ' '.join(heading[1:])
            baslik = ' '.join(heading.split()[:7])
            tarih = ' '.join(heading.split()[7:-1])
            detay = tidy(' '.join(response.css('div.row div.col-md-12 > '
                                               'p::text').getall())) or 'None'
            yield {
                'Url': response.request.url,
                'Baslik': baslik,
                'Tarih': tarih,
                'Detay': detay,
                'Yazar': '',
                'Haber / Kose Yazisi / Konusma': '',
            }
        else:
            new_url = response.url.replace('BitisSayfa=1',
                                           'BitisSayfa=' + page_count)
            yield scrapy.Request(new_url, callback=self.parse_page)

    def parse_page(self, response):
        if response.url == 'https://www.tbmm.gov.tr/bakim.htm':
            wrong_url = response.request.meta.get('redirect_urls')[0]
            print(wrong_url)
            last_page = re.search(r'(?<=BitisSayfa=)\d+', wrong_url)[0]
            if last_page == '2':
                raise ValueError(wrong_url)
            penul_page = int(last_page) - 1
            fixed_url = wrong_url.replace(f'BitisSayfa={last_page}',
                                          f'BitisSayfa={penul_page}')
            yield scrapy.Request(fixed_url, callback=self.parse_page)
        else:
            heading = [a.strip() for a in
                       response.css('span.main-area-title::text').getall()]
            heading = ' '.join(heading[1:])
            baslik = ' '.join(heading.split()[:7])
            tarih = ' '.join(heading.split()[7:-1])
            detay = tidy(' '.join(response.css('div.row div.col-md-12 > '
                                               'p::text').getall())) or 'None'
            yield {
                'Url': response.request.url,
                'Baslik': baslik,
                'Tarih': tarih,
                'Detay': detay,
                'Yazar': '',
                'Haber / Kose Yazisi / Konusma': '',
            }

# scrapy crawl tbmm -O tbmm.json --logfile spider.log --loglevel ERROR
