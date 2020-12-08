# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        for product in response.xpath("//div[@id='product-lists']/div"):
            yield {
                'product_url': product.xpath(".//div[@class='product-img-outer']/a/@href").get(),
                'product_img_link': product.xpath(".//div[@class='product-img-outer']/a/img/@data-src").get(),
                'product_name': product.xpath(".//div[@class='p-title']/a/@title").get(),
                'product_price': product.xpath(".//div[@class='p-price']//span/text()").get(),
            }

        next_page = response.xpath("//a[@rel='next']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
