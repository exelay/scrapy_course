# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
            assert(splash:go(args.url))
            assert(splash:wait(1))
            usd_tab = assert(splash:select_all(".filterPanelItem___2z5Gb "))
            usd_tab[3]:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
            return splash:png()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.livecoin.net/en', callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[@class='ReactVirtualized__Table__row tableRow___3EtiS ']"):
            yield {
                'currency_pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get(),
            }
