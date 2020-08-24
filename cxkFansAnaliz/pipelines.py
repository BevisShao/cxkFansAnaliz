# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import logging
import os
import time
from twisted.internet import defer, reactor

class CxkfansanalizPipeline(object):
    collection_name = 'cxkFans_items'
    logger = logging.getLogger(__name__)

    def __init__(self, mongo_uri, mongo_db, mongo_uri_docker):
        if os.getenv('ISDOCKER'):
            self.mongo_uri = mongo_uri_docker
            print('docker容器服务：mongodb')
        else:
            self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_uri_docker=crawler.settings.get('MONGO_URI_DOCKER')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, 27017)
        self.db = self.client[self.mongo_db]
        self.logger.info('open_spider()')

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self._insert, item, out)
        yield out
        defer.returnValue(item)
        self.logger.info('mongodb')
        # self.db[self.collection_name].insert(dict(item))
        # return item

    def _insert(self, item ,out):
        time.sleep(10)
        self.db[self.collection_name].insert(dict(item))
        reactor.callFromThread(out.callback, item)

    def close_spider(self, spider):
        self.client.close()


