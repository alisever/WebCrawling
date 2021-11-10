from os import remove
import scrapy
import datetime
import urllib


class SaleResidential(scrapy.Spider):
    name = 'zoopla'
    base_url = 'https://www.zoopla.co.uk/for-sale/property/'

    # search query parameters
    params = {
        'floor_area_units': 'sq_feet',
        'q': '',
        'radius': '0',  # search area miles
        'results_sort': 'lowest_price',
        'search_source': 'for-sale',
        'pn': '1'
    }

    # current page
    current_page = 1

    # postcodes list
    postcodes = []

    # constructor init
    def __init__(self):

        # init postcodes list
        content = ''
        with open('postcodes.csv', 'r') as f:
            for item in f:
                self.postcodes.append(item.strip('\n').replace(' ', ''))

    def start_requests(self):
        # init filename
        filename = './output/Residential_Sale_' + \
            datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.json'
        print(filename)

        # postcodes count
        count = 1

        # loop over postcodes
        for postcode in self.postcodes:
            self.current_page = 1
            self.params['q'] = postcode
            next_postcode = self.base_url + postcode.lower() + '/?' + \
                urllib.parse.urlencode(self.params)
            yield scrapy.Request(url=next_postcode, headers=self.headers,
                                 meta={'postcode': postcode,
                                       'filename': filename, 'count': count},
                                 callback=self.parse_links)
            count += 1

    def parse_links(self, response):

        # if response.css('div[content="No results found"]').getall():
        #    return

        cards = response.css('a[data-testid="listing-details-link"]')
        for link in cards:
            card_link = link.css('a').attrib['href']
            card_url = 'https://www.zoopla.co.uk' + str(card_link)
            price = link.css(
                'p[class="css-1o565rw-Text eczcs4p0"]::text').getall()
            title = link.css('h2[data-testid="listing-title"]::text').getall()
            listing_description = link.css(
                'p[data-testid="listing-description"]::text').getall()
            listing_features = link.css(
                'div[data-testid="listing-spec"] p[data-testid="text"]::text').getall()
            listing_transprot = link.css(
                'div[data-testid="listing-transport"] p[data-testid="text"]::text').getall()
            bedroom = ''
            bathroom = ''
            reception = ''

            yield {
                    'card_link': card_url,
                    'price': price,
                    'title': title,
                    'listing_description': listing_description,
                    'listing_features': listing_features,
                    'bedroom': bedroom,
                    'bathroom': bathroom,
                    'reception': reception,
                    'listing_transprot': listing_transprot
            }
