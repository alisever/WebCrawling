# import json
#
# from scrapy import Spider
#
#
# def tidy(text):
#     tidy_text = (text.replace('\r', '').replace('\n', '').replace('\t', '')
#                  .replace('\xa0', ' ').strip())
#     return tidy_text
#
#
# base = ''
#
#
# class AllSpider(Spider):
#     name = 'template1'
#
#     start_urls = [base]
#
#     def parse(self, response, **kwargs):
#         yield {
#             'link': response
#         }
#
#
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
