import json

import scrapy


base = 'https://www.akparti.org.tr/haberler/kategori/genel-baskan'


class AllSpider(scrapy.Spider):
    name = 'akp_all'
    start_urls = [base]
    page_no = 0

    def parse(self, response, **kwargs):
        self.page_no += 1
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,tr;q=0.7",
            "content-type": "application/json",
            "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-requested-with": "XMLHttpRequest"
        }

        payload = {
            "category": "27d14268-9f90-4830-b011-c48df5b97843",
            "page": self.page_no,
            "culture": "tr",
            "newsRootId": 1164,
            "tag": ""
        }
        if self.page_no == 1:
            for link in response.css('div.col-md-4.'
                                     'col-sm-6 a::attr(href)').getall():
                yield {
                    'link': 'https://www.akparti.org.tr' + link
                }
            yield scrapy.Request(
                'https://www.akparti.org.tr/cms/surface/NewsAjaxOperations/Get',
                method='POST',
                headers=headers,
                body=json.dumps(payload),
                callback=self.parse)
        else:
            hasan = json.loads(response.text)
            for item in hasan['Items']:
                yield {
                    'link': 'https://www.akparti.org.tr' + item['Url']
                }
            if hasan['HasNext']:
                yield scrapy.Request('https://www.akparti.org.tr/cms/surface/NewsAjaxOperations/Get',
                                     method='POST',
                                     headers=headers,
                                     body=json.dumps(payload),
                                     callback=self.parse)


with open('akp.json') as json_file:
    news_pages = json.load(json_file)


class SingleSpider(scrapy.Spider):
    name = 'akp'
    start_urls = [a.get('link') for a in news_pages[:10]]

    def parse(self, response, **kwargs):
            yield {
                'Url': response.request.url,
                'Baslik': response.css('div.content.clearfix.newsDetail > h1 ::text').get().replace("\r", "").replace("\n", "").replace("\xa0", " "),
                'Tarih': response.css('div.col-md-6 span ::text').get()[:-9],
                'Detay': ' '.join(response.css('div.content.clearfix.newsDetail > p ::text').getall()).replace("\r", "").replace("\n", "").replace("\xa0", " "),
            }


# class ExceptionSpider(scrapy.Spider):
#     name = 'yeni_safak_except'
#     start_urls = ['https://www.yenisafak.com/dusunce-gunlugu/'
#                   '15-temmuz-2016da-turkiyede-ne-oldu-2499421']
#
#     def parse(self, response, **kwargs):
#         yield {
#                 'Url': response.request.url,
#                 'Baslik': response.css('h1.title::text').get(),
#                 'Tarih': response.css('time.item.time::text').get().partition(
#                     ',')[0],
#                 'Detay': ''.join(response.css('[class^="text text"]::text'
#                                               ).getall()).strip(),
#                 'Yazar': response.css('div.text.text-666666 > strong::text').get()[1:],
#                 'Haber / Kose Yazisi / Konusma': 'Kose Yazisi'
#             }
