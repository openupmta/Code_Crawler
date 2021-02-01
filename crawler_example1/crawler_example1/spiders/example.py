from datetime import datetime, time

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
import logging
from crawler_example1.items import CrawlerExample1Item

# create logger
logger = logging.getLogger("ros")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("app.log")
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)


class ExampleSpider(scrapy.Spider):
    name = 'batdongsan'
    allowed_domains = ['batdongsan.com']
    start_urls = ['https://batdongsan.com.vn/nha-dat-ban']

    def parse(self, response):
        logger.info("Start crawler")

        yield Request(url='https://batdongsan.com.vn/nha-dat-ban',
                      callback=self.parsing_pages,
                      dont_filter=True)
        logger.info("Finish crawler")

    def parsing_pages(self, response):
        yield Request(url=response.url,
                      callback=self.page_info,
                      dont_filter=True)
        try:
            # Type is list
            pages = response.xpath('//*[@class="pagination"]').xpath('a').getall()
            # index current in list
            curr_page = response.xpath('//*[@class="pagination"]//a[@class="actived"]').get()
            # Get url next in list
            url = response.xpath('//*[@class="pagination"]').xpath('a')[pages.index(curr_page) + 1].xpath(
                '@href').extract_first()
            if url is not None:
                logger.info('Page : ' + url)
                yield Request(url='http://batdongsan.com.vn/' + url, callback=self.parsing_pages, dont_filter=True)
        except Exception as ex:
            print(ex.__str__())
            logger.error(ex.__str__())

    def page_info(self, response):
        try:
            body = response.xpath('//*[@class="vip1 product-item clearfix"]/a/@href')
            for info in body:
                url = info.get()
                logger.info('Crawler : ' + url)
                yield Request(url='http://batdongsan.com.vn/' + url, callback=self.extract_real_estate,
                              dont_filter=True)
        except Exception as e:
            print(e.__str__())
            logger.error(e.__str__())

    def extract_real_estate(self, response):

        address = self.address(response)
        price, acreage, room = self.dataset(response)
        loader = ItemLoader(item=CrawlerExample1Item(), response=response)
        loader.add_value('address', address)
        loader.add_value('price', price)
        loader.add_value('acreage', acreage)
        loader.add_value('room', room)
        return loader.load_item()

    @staticmethod
    def dataset(response):
        body = response.xpath('//*[@class="detail-2 pad-16"]').xpath('//li/span[@class="sp2"]/text()')
        try:

            price = body[0].extract()
        except Exception as ex:
            print(ex.__str__())
            logger.error(ex.__str__())
            price = None
        try:
            acreage = body[1].extract()
        except Exception as ex:
            print(ex.__str__())
            logger.error(ex.__str__())
            acreage = None
        try:
            room = body[2].extract()
        except Exception as ex:
            print(ex.__str__())
            logger.error(ex.__str__())
            room = None

        return price, acreage, room

    @staticmethod
    def movie_detail_processing(details, titles):
        x = {}
        for i in range(len(details)):
            title = titles[i]
            detail = details[i]
            a = {
                title[0].strip(":"): detail[0]
            }
            x.update(a)
        return x

    @staticmethod
    def address(response):
        address = response.xpath('//*[@class="short-detail"]/text()').extract_first()
        return address

    @staticmethod
    def image(response):
        body = response.xpath('//*[@class="movie-l-img"]')
        return body.xpath('img/@src').extract_first()
