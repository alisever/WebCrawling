import json

from scrapy import Spider, Request

base = 'https://www.zoopla.co.uk/for-sale/property/b1/' \
       '?floor_area_units=sq_feet&q=B1&radius=0&results_sort=lowest_price&' \
       'search_source=for-sale&pn={}'


class AllSpider(Spider):
    name = 'zoopla'
    start_urls = [base.format(1)]
    page_no = 1

    def parse(self, response, **kwargs):
        if response.css('div[content="No results found"]'):
            return

        for card in response.css('a[data-testid="listing-details-link"]'):
            yield {
                    'card_link': response.urljoin(card.css('a[data-testid="listing-details-link"]::attr(href)').get()),
                    'price': card.css('div[data-testid="listing-price"] ::text').getall()[-1][1:],
                    'title': card.css('h2[data-testid="listing-title"]::text').get(),
                    'listing_description': card.css('p[data-testid="listing-description"]::text').get(),
                    'listing_features': card.css('div[data-testid="listing-spec"] ::text').getall(),
                    'listing_transport': card.css('div[data-testid="listing-transport"] ::text').getall()
            }

        self.page_no += 1
        url = base.format(self.page_no)
        yield Request(url)

# scrapy crawl zoopla -O zoopla.json --logfile spider.log --loglevel ERROR
