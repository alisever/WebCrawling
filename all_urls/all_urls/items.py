# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class AllUrlsItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    keyword = scrapy.Field(output_processor=TakeFirst())
