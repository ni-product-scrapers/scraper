import pymongo
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb://scrapinghub:hackdays2019@ni-scraped-products-shard-00-00-njxbf.gcp.mongodb.net:27017,"
            "ni-scraped-products-shard-00-01-njxbf.gcp.mongodb.net:27017,"
            "ni-scraped-products-shard-00-02-njxbf.gcp.mongodb.net:27017/test?ssl=true&replicaSet=ni-scraped-products"
            "-shard-0&authSource=admin&retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
        self.database = 'scraped-products'
        self.collection = 'items'

    def process_item(self, item, spider):
        if item:
            collection = self.client.get_database(self.database).get_collection(self.collection)
            collection.find_one_and_update({"sku": item['sku'], "shop": item['shop']},
                                           {"$set": dict(item)}, upsert=True)
        else:
            raise DropItem("Missing {0}!".format(item))
        return item
