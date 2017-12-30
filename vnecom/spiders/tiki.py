# -*- coding:utf-8 -*-

import scrapy
from scrapy_splash import SplashRequest
from vnecom.items import ProductItem

class TikiSpider(scrapy.Spider):
  name = "tiki_spider"
  start_urls = [
    'https://tiki.vn/dien-thoai-may-tinh-bang/c1789',
    # 'http://localhost:8050/render.html?url=https://tiki.vn/dien-thoai-may-tinh-bang/c1789'
    # 'https://tiki.vn/dien-thoai-samsung-galaxy-a8-plus-2018-hang-chinh-hang-p1003657.html'
  ]

  def parse(self, response):
    products = response.css('div.product-box-list div a::attr("href")').extract()
    for product in products:
      yield response.follow(product, self.parse_item)

  def parse_item(self, response):
    product = ProductItem()
    product["url"] = response.url
    product["title"] = response.css('div.item-box h1.item-name::text').extract_first().strip()
    product["brand"] = response.css('div.item-brand p a::text').extract()
    product["short_description"] = response.css('div.top-feature-item p::text').extract()
    product["prices"] = response.css('input[name="price"]::attr(value)').extract()
    product["sku"] = response.css('input[name="product_sku"]::attr(value)').extract()

    # product["tags"] = response.css('div.product-detail__tag div.product-tag__list a::text').extract()

    yield product