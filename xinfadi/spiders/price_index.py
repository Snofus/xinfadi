from typing import Any, Iterable, Optional
import scrapy
import jsonpath
from scrapy import FormRequest
from scrapy.http import Request
import json


class PriceIndexSpider(scrapy.Spider):
    name = "price_index"
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.allowed_domains = ["xinfadi.com.cn"]
        self.page = 11620
        self.star_url = "http://www.xinfadi.com.cn/getPriceData.html"
        self.formdata = {"limit":"20","current":f"{self.page}"}

    def start_requests(self):
        print(f"---------起始页爬取: {self.page}------------")
        yield scrapy.FormRequest(url = self.star_url,callback = self.parse, method = 'POST',formdata=self.formdata)
    def parse(self, response):
        data = json.loads(response.body)
        items_data = data['list']
        for item in items_data:
            item_name = item['prodName']
            item_cat = item['prodCat']
            low_price = item['lowPrice']
            high_price = item['highPrice']
            avg_price = item['avgPrice']
            origin = item['place']
            date = item['pubDate']
            yield {
                "item_name" :item_name,
                "item_cat" :item_cat,
                "low_price" :low_price,
                "high_price" :high_price,
                "avg_price" :avg_price,
                "origin" :origin,
                "date" :date
            }
        if self.page < 29086:
            self.page += 1
            print(f"--------->目前正在爬取页书: {self.page}<-----------")
            self.formdata = {"limit":"20","current":f"{self.page}"}
            yield scrapy.FormRequest(url = self.star_url, callback = self.parse, method = "POST", formdata = self.formdata)
