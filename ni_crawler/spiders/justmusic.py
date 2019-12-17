# -*- coding: utf-8 -*-
import scrapy
from .. items import ProductItem
from scrapy.spiders import CrawlSpider

PRODUCT_PAGES = {
    'https://www.justmusic.de/Recording/Controller/Sonstige-Controller/Native-Instruments-Maschine-Mikro-MK3': {
        'name': 'Maschine Mikro MK3',
        'id': 'MaschineMikroMK3',
        'sku': 'MASCHINEMikroMk3',
    },
}


class JustMusicSpider(CrawlSpider):
    name = 'justmusic'
    allowed_domains = ['justmusic.de']

    def start_requests(self):
        for url in PRODUCT_PAGES.keys():
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        url = response.url

        item = ProductItem()

        item['shop'] = 'justmusic'
        item['country'] = 'DE'
        item['product_url'] = url
        item['name'] = PRODUCT_PAGES[url]['name']
        item['sku'] = PRODUCT_PAGES[url]['sku']
        price_block = response.css('.custom_buybox')
        item['price'] = price_block.css('[itemprop="price"]')[0].xpath('@content')[0].extract()
        item['currency'] = price_block.css('[itemprop="priceCurrency"]')[0].xpath('@content')[0].extract()

        item['image_url'] = response.css('[itemprop="image"]')[0].xpath('@src').extract()[0]

        yield item