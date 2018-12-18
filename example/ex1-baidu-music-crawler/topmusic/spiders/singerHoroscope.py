# -*- coding: utf-8 -*-
import scrapy


class SingerHoroscopeSpider(scrapy.Spider):
    name = 'singerHoroscope'
    start_urls = ['http://music.baidu.com/top/dayhot/']

    def parse(self, response):
        song_items = response.css('.song-item')

        def extract_by_css(parent, selector):
            return [s.strip() if s else '-' for s in parent.css(selector).extract()]

        for song in song_items:
            for singer in song.css('.author_list a'):
                req = response.follow(singer, callback=self.parse_singer)
                req.meta['song'] = {
                    'rank': extract_by_css(song, '.index-num::text'),
                    'title': extract_by_css(song, '.song-title > a:first-child::text'),
                }
                yield req

    def parse_singer(self, response):
        horoscope = response.css('span.birth').re_first(u'..座') or '-'
        yield {
            'singer': response.css('.artist-name::text').extract(),
            'horoscope': horoscope.strip(),
            'rank': response.meta['song']['rank'],
            'title': response.meta['song']['title'],
        }
