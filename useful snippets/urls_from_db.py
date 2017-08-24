#
# This file was created by Attila Toth - http://scrapingauthority.com
#
#
# This snippet is usable to request URLs that are already defined in a database.
# This template assumes that you've created an API endpoint (JSON) for the URLs which looks like this:
#
#[
#    {
#        "product_id": 1
#        "shop1": "https://www.url1.com",
#        "shop2": "https://www.url2.com",
#        "shop3": "https://www.url3.com"
#
#    },
#    ...
#]
# Later these URLs will be scraped by Scrapy then the product_id and shop name will be passed as meta parameters
#
#


import requests
from scrapy import Request
from scrapy.loader import ItemLoader


class MySpider(Spider):
    name = ''
    start_urls = [] #no start_urls

    def start_requests(self):
        products = requests.get("mywebsite.com/myapi").json()
        for product in products:
            product_id = product["product_id"]
            for key, value in product.iteritems():
                if key == "product_id":
                    continue
                if value is not None:
                    yield Request(url=value, meta={"product_id": product_id, "shop": key})

    # 1. SCRAPING
    def parse(self, response):
        item_loader = ItemLoader(item=MyItem(), response=response)

        #item_loader.add_css("", "")
        #item_loader.add_value("product_id", response.meta["product_id"])

        return item_loader.load_item()