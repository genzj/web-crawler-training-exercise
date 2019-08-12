# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class SimpleloginSpider(scrapy.Spider):
    name = 'simplelogin'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
        'http://quotes.toscrape.com/page/3/'
    ]

    login_url = 'http://quotes.toscrape.com/login'

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login_auto)
        # or...
        # yield scrapy.Request(self.login_url, callback=self.login_manual)

    def login_auto(self, response):
        request = FormRequest.from_response(
            response,
            callback=self.landing_page,
            formdata={
                'username': 'testuser',
                'password': 'password',
            }
        )
        yield request

    def login_manual(self, response):
        token = response.css(
            'input[name=csrf_token]::attr(value)'
        ).extract_first()
        post_url = response.css('form::attr(action)').extract_first()
        self.logger.debug('post to %s, csrf token is %s', post_url, token)

        yield response.follow(
            url=post_url,
            callback=self.landing_page,
            method='POST',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body=urlencode({
                'csrf_token': token,
                'username': 'testuser',
                'password': 'password',
            }),
        )

    def landing_page(self, response):
        logout_link = response.css('a[href="/logout"]')
        self.logger.debug('logout_link=%r', logout_link)
        assert len(logout_link) >= 1, 'Login failed!'

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('.quote'):
            yield {
                'text': quote.css('.text::text').extract_first().strip(),
                'by': quote.css('.author::text').extract_first().strip(),
            }
