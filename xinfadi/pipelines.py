# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class XinfadiPipeline:
    
    def open_spider(self,spider):
        print("与DB的链接已建立......")
        self.client = MongoClient("127.0.0.1",27017)
    def process_item(self, item, spider):
        print("-----已收到数据，可以储备------")
        collection = self.client['crawler']['xinfadi']
        collection.insert_one(item)
    def close_spider(self,spider):
        self.client.close()
        print("与DB的链接已关闭......")