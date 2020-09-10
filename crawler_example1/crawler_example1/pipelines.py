# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from pymongo import MongoClient
from bson.objectid import ObjectId
from crawler_example1.settings import MONGODB_COLLECTION, MONGODB_DB, MONGODB_HOST, MONGODB_PORT
from crawler_example1.spiders.example import logger

class CrawlerExample1Pipeline(object):

    def __init__(self):
        connection = MongoClient(
            MONGODB_HOST,
            MONGODB_PORT)
        self.db = connection[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert({"_id": ObjectId().__str__(),
                                'address': item['address'][0],
                                'price': item['price'][0],
                                'acreage': item['acreage'][0],
                                'room': item['room'][0]})
        logger.info(item['address'][0])
        return item