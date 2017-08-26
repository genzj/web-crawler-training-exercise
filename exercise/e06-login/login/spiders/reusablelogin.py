# -*- coding: utf-8 -*-
import scrapy

from urllib import urlencode

class ReusableLoginSpider(scrapy.Spider):
    login_url = ''
    user_form_name = 'username'

    password_form_name = 'password'

    user_form_value = None
    password_form_value = None

    def start_requests(self):
        if self.user_form_value is None or self.password_form_value is None:
            raise ValueError('user_form_value and password_form_value should be specified.')

        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        tokens = response.css('input[type=hidden]')
        post_url = response.css('form::attr(action)').extract_first()

        form_data = {
            self.user_form_name: self.user_form_value,
            self.password_form_name: self.password_form_value,
        }
        self.logger.debug('post to %s, data %s', post_url, form_data)

        for token in tokens:
            form_data[token.css('::attr(name)').extract_first()] = token.css('::attr(value)').extract_first()

        yield response.follow(
            url=post_url,
            callback=self.landing_page,
            method='POST',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body=urlencode(form_data),
        )

    def landing_page(self, response):
        raise NotImplementedError('subclass should implement this method to parse first page after login')


class LoginQuotaSpider(ReusableLoginSpider):
    name = 'loginquota'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
        'http://quotes.toscrape.com/page/3/'
    ]

    login_url = 'http://quotes.toscrape.com/login'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        cls.user_form_value = crawler.settings.get('LOGIN_USERNAME', None)
        cls.password_form_value = crawler.settings.get('LOGIN_PASSWORD', None)
        return super(LoginQuotaSpider, cls).from_crawler(crawler, *args, **kwargs)

    def landing_page(self, response):
        errors = response.css('.error::text').extract()
        if errors:
            self.logger.warning('error encountered in landing page: %s', errors)

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
