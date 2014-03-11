import pymongo
import settings
from scrapy import log

class MongoDBPipeline(object):
    def __init__(self):
        self.server = settings.MONGODB_SERVER
        self.port = settings.MONGODB_PORT
        self.db = settings.MONGODB_DB
        self.col = settings.MONGODB_COLLECTION

        connection = pymongo.Connection(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),
                level=log.DEBUG, spider=spider)
        return item
