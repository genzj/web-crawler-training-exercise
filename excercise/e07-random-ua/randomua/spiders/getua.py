# -*- coding: utf-8 -*-
import scrapy


class GetuaSpider(scrapy.Spider):
    name = 'getua'
    allowed_domains = ['whatsmyua.info']
    start_urls = ['http://www.whatsmyua.info/']

    def parse(self, response):
        yield {
            'User Agent': response.css('#custom-ua-string::text').extract_first(),
            'Name': response.css('#family::text').re_first(r'family: (.*)'),
        }
