# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuotesJsSpider(scrapy.Spider):
    name = 'quotes_js'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
    function main(splash, args)
      assert(splash:go(args.url))
      assert(splash:wait(1))
      return splash:html()
    end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://quotes.toscrape.com/js/', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath(".//span[1]/text()").get(),
                'author': quote.xpath(".//span[2]/small/text()").get(),
                'tags': quote.xpath(".//div/a/text()").getall(),
            }
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            absolute_url = f"https://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })
