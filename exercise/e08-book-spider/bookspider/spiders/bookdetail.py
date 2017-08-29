# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BookItemLoader


class BookdetailSpider(CrawlSpider):
    name = 'bookdetail'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        # Rule(LinkExtractor(
        #         restrict_css='.sidebar',
        #         deny=(
        #             '/catalogue/category/books_1/index.html',
        #         ),
        #     ),
        # ),
        Rule(LinkExtractor(restrict_css='li.next')),
        Rule(LinkExtractor(restrict_css='ol'), callback='parse_book')
    )

    def parse_book(self, response):
        loader = BookItemLoader(response=response)
        loader.add_css('category', '.breadcrumb li:nth-child(3) a::text')
        loader.add_value('url', response.url)
        detail_loader = loader.nested_css('.product_main')
        detail_loader.add_css('name', 'h1::text')
        detail_loader.add_css('price', '.price_color')
        detail_loader.add_css('availability', '.availability')
        detail_loader.add_css('stock', '.availability', re=r'\((\d+) available\)')
        detail_loader.add_css('star', '.star-rating::attr(class)')
        yield loader.load_item()