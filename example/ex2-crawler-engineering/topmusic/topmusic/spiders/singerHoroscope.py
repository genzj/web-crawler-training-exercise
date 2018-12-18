# -*- coding: utf-8 -*-
import scrapy
from ..itemloaders import SingerHoroscopeItemLoader, SongItemLoader


class SingerhoroscopeSpider(scrapy.Spider):
    name = 'singerHoroscope'
    start_urls = ['http://music.baidu.com/top/dayhot/']

    def parse(self, response):
        song_items = response.css('.song-item')

        for song in song_items[:10]:
            item = SongItemLoader.parse_top_song(song)
            self.logger.debug('parsed song: %s', item)
            for url in item['singer_urls']:
                req = response.follow(url, callback=self.parse_singer)
                req.meta['song'] = item
                yield req

    def parse_singer(self, response):
        return SingerHoroscopeItemLoader.parse_singer_page(response)

