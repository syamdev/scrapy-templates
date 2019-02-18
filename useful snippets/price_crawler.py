#
# This file was created by Attila Toth - http://scrapingauthority.com
#
#
# This snippet is usable to request URLs that are already defined in a database.
# This template assumes that you've created an API endpoint (JSON) for the URLs which looks like this:
#
#[
#    {
#        "ProductId": 1
#        "Url": "https://www.url1.com"
#    },
#    ...
#]
# Later these URLs will be scraped by Scrapy then the ProductId will be passed as meta parameter
#
#

import uuid
import datetime
import requests
from scrapy import Request
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from PriceCrawler.custom_items import *

class PriceSpider(Spider):

    name = "price_crawler"

    def __init__(self, **kwargs):
        # Arguments from command line
        self.price_css = kwargs.get("price_css")
        self.stock_css = kwargs.get("stock_css")
        self.shop_id = kwargs.get("shop_id")
        self.cron_id = kwargs.get("cron_id")
        self.app_url = kwargs.get("app_url")
        self.apikey = kwargs.get("apikey")
        super(PriceSpider, self).__init__(**kwargs)

    def start_requests(self):
        products_api = ("{app_url}/api/products?apikey={apikey}&shop_id={shop_id}"
                        ).format(app_url=self.app_url, apikey=self.apikey, shop_id=self.shop_id)
        products = requests.get(products_api).json()
        for product in products:
            url = product.get("Url")
            meta_data = {"product_id": product.get("ProductId")}
            yield Request(url=url, meta=meta_data)

    # 1. Scraping using the given css selectors
    def parse(self, response):
        item = PriceItem()
        item_loader = ItemLoader(item=item, response=response)
        item_loader.default_output_processor = TakeFirst()
        
        item_loader.add_css("price", self.price_css)
        item_loader.add_css("stock", self.stock_css)

        item_loader.add_value("product_id", response.meta.get("product_id"))
        item_loader.add_value("cron_id", self.cron_id)
        item_loader.add_value("shop_id", self.shop_id)
        item_loader.add_value("item_id", str(uuid.uuid1()))
        item_loader.add_value("updated", str(datetime.datetime.now()))
        item_loader.add_value("url", response.url)

        return item_loader.load_item()

    # 2. Updating database by calling the backend API
    def closed(self, reason):
        db_ubdate_url = "{app_url}/api/update?apikey={apikey}".format(app_url=self.app_url, apikey=self.apikey)
        requests.get(db_ubdate_url)
