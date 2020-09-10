# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerExample1Item(scrapy.Item):
    address = scrapy.Field()
    price = scrapy.Field()
    acreage = scrapy.Field()
    room = scrapy.Field()
