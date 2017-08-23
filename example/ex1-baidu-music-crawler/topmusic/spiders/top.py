# -*- coding: utf-8 -*-

import scrapy


class TopSpider(scrapy.Spider):
    name = 'top'
    start_urls = ['http://music.baidu.com/top/dayhot']

    def parse(self, response):
        def extract_by_css(selector):
            return response.css(selector).extract()

        for rank, title, singer in zip(
            extract_by_css('.index-num.index-hook::text'),
            extract_by_css('.song-title > a:first-child::text'),
            extract_by_css('.author_list::attr(title)'),
        ):
            yield {
                'rank': rank,
                'title': title.strip(),
                'singer': singer.strip().strip('"')
            }

