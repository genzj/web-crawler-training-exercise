# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SingerHoroscopeItem(scrapy.Item):
    singer = scrapy.Field()
    horoscope = scrapy.Field()
    rank = scrapy.Field()
    title = scrapy.Field()
    sign = scrapy.Field()


class SongItem(scrapy.Item):
    singer_urls = scrapy.Field()
    title = scrapy.Field()
    rank = scrapy.Field()
