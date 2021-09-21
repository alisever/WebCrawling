import scrapy


class FetoSpider(scrapy.Spider):
    name = 'feto'
    start_urls = ['https://www.ensonhaber.com/arama/?q=fet%C3%B6']
    page_no = 1

    def parse(self, response, **kwargs):
        if self.page_no == 1:
            for news in response.css('div.news-container.js-ci').css('a'):
                yield {
                    'link': news.attrib['href']
                }
        else:
            for news in response.css('a'):
                yield {
                    'link': news.attrib['href']
                }

        if self.page_no < 1000:
            url = f'https://www.ensonhaber.com/arama/?q=fetö&sayfa=' \
                  f'{self.page_no}&infinity=1'
            self.page_no += 1
            try:
                yield scrapy.Request(url, method='POST')
            except:
                return