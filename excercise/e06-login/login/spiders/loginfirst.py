# -*- coding: utf-8 -*-
import scrapy


class LoginfirstSpider(scrapy.Spider):
    name = 'loginfirst'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
        'http://quotes.toscrape.com/page/3/'
    ]

    login_url = 'http://quotes.toscrape.com/login'

    def start_requests(self):
        return super(LoginfirstSpider, self).start_requests()

    def parse(self, response):
        pass
