# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class ReusableLoginSpider(scrapy.Spider):
    login_url = ''
    user_form_name = 'username'
    password_form_name = 'password'

    def start_requests(self):
        username = self.settings.get('LOGIN_USERNAME')
        password = self.settings.get('LOGIN_PASSWORD')
        if not username or not password:
            raise ValueError(
                'LOGIN_USERNAME and LOGIN_PASSWORD should be specified in settings.')

        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        username = self.settings.get('LOGIN_USERNAME')
        password = self.settings.get('LOGIN_PASSWORD')
        request = FormRequest.from_response(
            response,
            callback=self.landing_page,
            formdata={
                self.user_form_name: username,
                self.password_form_name: password,
            }
        )
        self.logger.debug('login %s as user %s', self.login_url, username)
        yield request

    def landing_page(self, response):
        raise NotImplementedError(
            'subclass should implement this method'
            ' to parse first page after login'
        )


class LoginQuotaSpider(ReusableLoginSpider):
    name = 'loginquota'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
        'http://quotes.toscrape.com/page/3/'
    ]

    login_url = 'http://quotes.toscrape.com/login'

    def landing_page(self, response):
        errors = response.css('.error::text').extract()
        if errors:
            self.logger.warning(
                'error encountered in landing page: %s',
                errors
            )

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
