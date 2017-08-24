#
# This file was created by Attila Toth - http://scrapingauthority.com
#
#
# This template is usable for pages where POST request needed to reach all fields from multiple pages.
#
#

from scrapy import FormRequest
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import Spider
from w3lib.html import remove_tags


class MySpider(Spider):
    name = ''
    start_urls = ['']  # LEVEL 1

    # 1. FOLLOWING LEVEL 1
    def parse(self, response):
        item_loader = ItemLoader(item=MyItem(), response=response)
        item_loader.default_input_processor = MapCompose(remove_tags)
        #item_loader.add_css("", "")
        #item_loader.add_css("", "")
        #item_loader.add_css("", "")
        yield FormRequest("POST_URL", formdata={'parameter': 'p'},
                                        meta={'item': item_loader.load_item()}, callback=self.populate_field)

    def populate_field(self, response):
        item_loader = ItemLoader(item=response.meta["item"], response=response)
        item_loader.default_input_processor = MapCompose(remove_tags)
        #item_loader.add_css("field", "")
        return item_loader.load_item()
