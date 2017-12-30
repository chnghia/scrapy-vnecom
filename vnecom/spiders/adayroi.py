import scrapy
from vnecom.items import ProductItem

class AdayroiSpider(scrapy.Spider):
  name = "adayroi_spider"
  start_urls = [
    'https://www.adayroi.com/dien-may-cong-nghe-c321',
    # 'https://www.adayroi.com/tu-lanh-toshiba-gr-wg66vdaz-gg-loai-lon-600-lit-p-PRI31487',
  ]

  def parse(self, response):
    products = response.css('div.product-item__info a.product-item__info-title::attr("href")').extract()
    for product in products:
      yield response.follow(product, self.parse_item)

  def parse_item(self, response):
    product = ProductItem()
    product["url"] = response.url
    product["title"] = response.css('div.product-detail__info div.product-detail__title h1::text').extract_first()
    product["brand"] = response.css('div.product-detail__info div.product-detail__title-brand a::text').extract()
    product["short_description"] = response.css('div.product-detail__info div.short-des__content ul li p::text').extract()
    product["prices"] = response.css('div.product-detail__price-info span::text').extract()
    product["tags"] = response.css('div.product-detail__tag div.product-tag__list a::text').extract()

    yield product