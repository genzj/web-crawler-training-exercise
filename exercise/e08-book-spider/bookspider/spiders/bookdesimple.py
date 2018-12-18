# -*- coding: utf-8 -*-
import scrapy


class BookdesimpleSpider(scrapy.Spider):
    name = 'booksimple'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for link in response.css('li.next a'):
            yield response.follow(link)
        for link in response.css('ol a'):
            yield response.follow(link, callback=self.parse_detail)

    def parse_detail(self, response):
        detail = response.css('.product_main')
        yield {
            'category': response.css('.breadcrumb li:nth-child(3) a::text').extract_first(),
            'url': response.url,
            'name': detail.css('h1::text').extract_first(),
            'price': float(detail.css('.price_color').re_first('([0-9.]+)')),
            'availability': 'in stock' in (detail.css('.availability::text').extract_first().lower()),
            'stock': detail.css('.availability').re_first(r'\((\d+) available\)'),
        }

