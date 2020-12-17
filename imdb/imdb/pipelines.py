# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongodbPipeline:
    # collection_name = "best_movies"

    @classmethod
    def from_crawler(cls, crawler):
        collection_name = crawler.settings.get("TOKEN")
        return cls(collection_name)

    def __init__(self, collection_name):
        self.collection_name = collection_name

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://imdb:rowdy0987@cluster0.mskrx.mongodb.net/<dbname>?retryWrites=true&w=majority"
        )
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
