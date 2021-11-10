from scrapy import Spider


class RollBackSpider(Spider):
    name = 'rollback'

    start_urls = ['https://groceries.asda.com/event/rollback']

    def parse(self, response, **kwargs):
        yield {
            'title': '',
            'price': '',
            'discounted_price': '',
            'description': '',
            'product_image_url': '',
            'product_url': ''
        }


# scrapy crawl template2 -O template.json --logfile spider.log --loglevel ERROR
